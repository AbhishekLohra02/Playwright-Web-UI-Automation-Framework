import pytest
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.messages import INVENTORY_REQUIRES_LOGIN

pytestmark = [pytest.mark.login, pytest.mark.regression]


@pytest.mark.smoke
@pytest.mark.sanity
def test_inventory_is_not_reachable_without_logging_in(page: Page) -> None:
    page.goto(InventoryPage.url_path)

    login_page = LoginPage(page)

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_have_text(INVENTORY_REQUIRES_LOGIN)
    expect(InventoryPage(page).inventory_list).to_have_count(0)
