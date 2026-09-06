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
    login_page.login(STANDARD_USERNAME, PASSWORD)
    return InventoryPage(login_page.page)


@pytest.fixture
def cart_with_products(logged_in_inventory_page: InventoryPage) -> CartPage:
    """Standard user with the selected products added, viewing the cart."""
    for product_name in CART_PRODUCTS:
        logged_in_inventory_page.add_product_to_cart(product_name)

    logged_in_inventory_page.open_cart()
    return CartPage(logged_in_inventory_page.page)


@pytest.fixture
def checkout_information_page(
    cart_with_products: CartPage,
) -> CheckoutInformationPage:
    """Checkout started, waiting on customer information."""
    cart_with_products.start_checkout()
    return CheckoutInformationPage(cart_with_products.page)


@pytest.fixture
def checkout_overview_page(
    checkout_information_page: CheckoutInformationPage,
) -> CheckoutOverviewPage:
    """Valid customer information submitted, showing the order overview."""
    checkout_information_page.enter_details(FIRST_NAME, LAST_NAME, POSTAL_CODE)
    checkout_information_page.click_continue()
    return CheckoutOverviewPage(checkout_information_page.page)


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
