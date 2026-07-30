import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def base_url():
    return "https://www.saucedemo.com/"


@pytest.fixture(scope="session", autouse=True)
def configure_test_id_attribute(playwright):
    playwright.selectors.set_test_id_attribute("data-test")

@pytest.fixture(scope="function")
def login_page(page: Page, base_url: str) -> LoginPage:
    login = LoginPage(page)
    login.open(base_url)
    return login