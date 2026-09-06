import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.users import PASSWORD, STANDARD_USERNAME

pytestmark = [pytest.mark.login, pytest.mark.regression]


@allure.epic("Authentication")
@allure.feature("Sign in")
@allure.story("The standard account reaches the catalogue")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
@pytest.mark.sanity
def test_successful_login_with_standard_user(login_page: LoginPage) -> None:
    login_page.login(STANDARD_USERNAME, PASSWORD)

    inventory_page = InventoryPage(login_page.page)

    inventory_page.expect_loaded()
    expect(inventory_page.page_title).to_be_visible()
    expect(inventory_page.page_title).to_have_text("Products")
