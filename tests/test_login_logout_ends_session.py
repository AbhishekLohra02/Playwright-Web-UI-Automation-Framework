import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from test_data.messages import INVENTORY_REQUIRES_LOGIN

pytestmark = [pytest.mark.login, pytest.mark.regression]


@allure.feature("Session handling")
@allure.story("Signing out ends the session")
@pytest.mark.sanity
def test_logout_ends_the_session_and_blocks_the_inventory(
    logged_in_inventory_page: InventoryPage,
) -> None:
    login_page = logged_in_inventory_page.header.logout()

    login_page.expect_loaded()
    expect(login_page.login_button).to_be_visible()

    login_page.page.goto(InventoryPage.url_path)

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_have_text(INVENTORY_REQUIRES_LOGIN)
