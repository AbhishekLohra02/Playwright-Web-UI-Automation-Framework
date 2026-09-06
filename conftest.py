from collections.abc import Callable, Generator
from typing import Any
from urllib.parse import urlparse

import allure
import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page, Playwright, expect

from pages.cart_page import CartPage
from pages.checkout_information_page import CheckoutInformationPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.customers import FIRST_NAME, LAST_NAME, POSTAL_CODE
from test_data.products import CART_PRODUCTS
from test_data.users import STANDARD_USERNAME

# One source of truth for the area a test belongs to. The pytest marker drives
# both selection (`-m checkout`) and the Allure epic, so the two can never
# disagree and no test has to repeat itself in a decorator.
# Timeouts are configured explicitly rather than left to Playwright's defaults.
# A loaded CI runner is the usual cause of a "flaky" UI suite, and an implicit
# 5-second assertion budget is a decision nobody made.
ASSERTION_TIMEOUT_MS = 10_000
ACTION_TIMEOUT_MS = 15_000
NAVIGATION_TIMEOUT_MS = 30_000

# SauceDemo keeps the signed-in user in this cookie and nothing else.
SESSION_COOKIE = "session-username"

# Accessibility impacts that fail a build. Moderate and minor findings are
# reported and tracked, but blocking on them would stall delivery for issues
# that do not stop anyone using the site.
BLOCKING_ACCESSIBILITY_IMPACTS = frozenset({"critical", "serious"})

AREA_EPICS = {
    "login": "Authentication",
    "inventory": "Product catalogue",
    "cart": "Shopping cart",
    "checkout": "Checkout",
}

# Test level implies how much a failure matters.
LEVEL_SEVERITIES = {
    "smoke": allure.severity_level.BLOCKER,
    "sanity": allure.severity_level.CRITICAL,
}


def pytest_configure(config: pytest.Config) -> None:
    """Make the `base_url` ini value reach pytest-xdist workers.

    pytest-base-url skips its own configure hook on worker nodes, so under
    `-n auto` the ini value never reaches the Playwright browser context and
    every relative navigation fails. Copying it here keeps parallel runs
    behaving exactly like serial ones, while still allowing --base-url and
    PYTEST_BASE_URL to win.
    """
    if config.getoption("base_url") is None:
        config.option.base_url = config.getini("base_url")


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Derive Allure metadata from the markers a test already has.

    Epic, severity and manual-case traceability all come from markers, so the
    same declaration drives test selection and the report. Nothing has to be
    restated in a decorator, and the two cannot drift apart.
    """
    for item in items:
        marker_names = {marker.name for marker in item.iter_markers()}

        for marker in item.iter_markers(name="manual_case"):
            for case_id in marker.args:
                item.add_marker(allure.tag(case_id))
                item.add_marker(allure.label("manual_case", case_id))

        for marker_name, epic in AREA_EPICS.items():
            if marker_name in marker_names:
                item.add_marker(allure.epic(epic))
                break

        severity = next(
            (
                LEVEL_SEVERITIES[level]
                for level in ("smoke", "sanity")
                if level in marker_names
            ),
            allure.severity_level.NORMAL,
        )
        item.add_marker(allure.severity(severity))


@pytest.fixture(scope="session", autouse=True)
def configure_test_id_attribute(playwright: Playwright) -> None:
    playwright.selectors.set_test_id_attribute("data-test")
    expect.set_options(timeout=ASSERTION_TIMEOUT_MS)


@pytest.fixture(autouse=True)
def configure_timeouts(page: Page) -> None:
    page.set_default_timeout(ACTION_TIMEOUT_MS)
    page.set_default_navigation_timeout(NAVIGATION_TIMEOUT_MS)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.open()
    return login


@pytest.fixture
def logged_in_inventory_page(page: Page, base_url: str) -> InventoryPage:
    """A signed-in session, established without driving the login form.

    Seeding the session cookie keeps a broken login page from failing every
    cart and checkout test as well; those then fail only when cart or checkout
    is genuinely broken, which is what makes a red build diagnosable. The login
    form itself is covered thoroughly by the authentication suite.

    This is not a speed optimisation - a UI sign-in measures 0.58s against
    0.54s for a seeded one. The benefit is failure isolation.
    """
    page.context.add_cookies(
        [
            {
                "name": SESSION_COOKIE,
                "value": STANDARD_USERNAME,
                "domain": urlparse(base_url).hostname or "",
                "path": "/",
            }
        ]
    )

    inventory_page = InventoryPage(page)
    inventory_page.open()
    inventory_page.expect_loaded()
    return inventory_page


@pytest.fixture
def cart_with_products(logged_in_inventory_page: InventoryPage) -> CartPage:
    """Standard user with the selected products added, viewing the cart."""
    for product_name in CART_PRODUCTS:
        logged_in_inventory_page.add_product_to_cart(product_name)

    return logged_in_inventory_page.header.open_cart()


@pytest.fixture
def checkout_information_page(
    cart_with_products: CartPage,
) -> CheckoutInformationPage:
    """Checkout started, waiting on customer information."""
    return cart_with_products.start_checkout()


@pytest.fixture
def checkout_overview_page(
    checkout_information_page: CheckoutInformationPage,
) -> CheckoutOverviewPage:
    """Valid customer information submitted, showing the order overview."""
    checkout_information_page.enter_details(FIRST_NAME, LAST_NAME, POSTAL_CODE)
    return checkout_information_page.continue_to_overview()


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, pytest.TestReport, pytest.TestReport]:
    """Attach the failing browser state to the Allure report.

    A screenshot and the URL at the moment of failure remove most of the
    guesswork when triaging a red build, especially one that only reproduces
    on CI.
    """
    report = yield

    if report.when != "call" or not report.failed:
        return report

    if not isinstance(item, pytest.Function):
        return report

    page = item.funcargs.get("page")
    if not isinstance(page, Page) or page.is_closed():
        return report

    allure.attach(
        page.url,
        name="URL at failure",
        attachment_type=allure.attachment_type.TEXT,
    )
    allure.attach(
        page.screenshot(full_page=True),
        name="Screenshot at failure",
        attachment_type=allure.attachment_type.PNG,
    )
    return report


@pytest.fixture
def accessibility_scan(
    page: Page,
) -> Callable[[str], list[dict[str, Any]]]:
    """Run axe-core against the current page and return blocking violations.

    The full axe report is attached to Allure either way, so moderate findings
    stay visible even though they do not fail the build.
    """
    axe = Axe()

    def scan(screen_name: str) -> list[dict[str, Any]]:
        results = axe.run(page)

        allure.attach(
            results.generate_report(),
            name=f"axe-core report - {screen_name}",
            attachment_type=allure.attachment_type.TEXT,
        )

        return [
            violation
            for violation in results.response["violations"]
            if violation["impact"] in BLOCKING_ACCESSIBILITY_IMPACTS
        ]

    return scan
