import allure
import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.checkout_information_page import CheckoutInformationPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.customers import FIRST_NAME, LAST_NAME, POSTAL_CODE
from test_data.products import CART_PRODUCTS
from test_data.users import PASSWORD, STANDARD_USERNAME

# One source of truth for the area a test belongs to. The pytest marker drives
# both selection (`-m checkout`) and the Allure epic, so the two can never
# disagree and no test has to repeat itself in a decorator.
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
    """Derive Allure epic and severity from the markers a test already has."""
    for item in items:
        marker_names = {marker.name for marker in item.iter_markers()}

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
def configure_test_id_attribute(playwright) -> None:
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.open()
    return login


@pytest.fixture
def logged_in_inventory_page(login_page: LoginPage) -> InventoryPage:
    return login_page.login_as(STANDARD_USERNAME, PASSWORD)


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


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Attach the failing browser state to the Allure report.

    A screenshot and the URL at the moment of failure remove most of the
    guesswork when triaging a red build, especially one that only reproduces
    on CI.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None or page.is_closed():
        return

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
