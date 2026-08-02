import pytest
from playwright.sync_api import Page

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.users import PASSWORD, STANDARD_USERNAME


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://www.saucedemo.com/"


@pytest.fixture(scope="session", autouse=True)
def configure_test_id_attribute(playwright) -> None:
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="function")
def login_page(page: Page, base_url: str) -> LoginPage:
    login = LoginPage(page)
    login.open(base_url)
    return login


@pytest.fixture(scope="function")
def logged_in_inventory_page(login_page: LoginPage) -> InventoryPage:
    login_page.login(STANDARD_USERNAME, PASSWORD)
    return InventoryPage(login_page.page)

