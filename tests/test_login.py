from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.users import PASSWORD, STANDARD_USERNAME


def test_successful_login_with_standard_user(
    login_page: LoginPage,
    base_url: str,
) -> None:
    login_page.login(STANDARD_USERNAME, PASSWORD)

    inventory_page = InventoryPage(login_page.page)

    expect(inventory_page.page_title).to_be_visible()
    expect(login_page.page).to_have_url(f"{base_url}inventory.html")
    expect(inventory_page.page_title).to_have_text("Products")
