from playwright.sync_api import Page
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from test_data.users import STANDARD_USERNAME, PASSWORD

## TC-AUTH-001

def test_successful_login_with_standard_user(login_page: LoginPage, base_url: str) -> None:
    inventory_page = InventoryPage(login_page.page)
    login_page.login(STANDARD_USERNAME, PASSWORD)
    expect(inventory_page.page_title).to_be_visible()
    expect(inventory_page.page_title).to_have_text("Products")


