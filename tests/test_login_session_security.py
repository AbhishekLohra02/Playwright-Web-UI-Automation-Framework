import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.messages import INVENTORY_REQUIRES_LOGIN

pytestmark = [pytest.mark.login, pytest.mark.regression]


@allure.epic("Authentication")
@allure.feature("Session handling")
@allure.story("A signed-out session cannot be restored")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.sanity
def test_browser_back_does_not_restore_a_signed_out_session(
    logged_in_inventory_page: InventoryPage,
) -> None:
    """Signing out must survive the browser Back button.

    A cached authenticated page served after logout is a genuine session
    weakness, and Back is the way a real user would stumble into it.
    """
    logged_in_inventory_page.logout()

    login_page = LoginPage(logged_in_inventory_page.page)
    login_page.expect_loaded()

    login_page.page.go_back()

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_have_text(INVENTORY_REQUIRES_LOGIN)
    expect(InventoryPage(login_page.page).inventory_list).to_have_count(0)
