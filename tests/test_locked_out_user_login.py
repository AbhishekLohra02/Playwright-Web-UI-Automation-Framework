from playwright.sync_api import Page
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from test_data.users import LOCKED_OUT_USERNAME, PASSWORD

# TC-AUTH-002
def test_locked_out_user_login(page: Page, base_url: str) -> None:
    locked_out_login = LoginPage(page)
    inventory_page = InventoryPage(page)

    locked_out_login.open(base_url)
    locked_out_login.login(LOCKED_OUT_USERNAME, PASSWORD)
    expect(locked_out_login.error_message).to_be_visible()
    
