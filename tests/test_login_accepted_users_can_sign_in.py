import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.users import PASSWORD, SIGN_IN_ENABLED_USERNAMES

pytestmark = [pytest.mark.login, pytest.mark.regression]


@allure.epic("Authentication")
@allure.feature("Sign in")
@allure.story("Every advertised account reaches the catalogue")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.sanity
@pytest.mark.parametrize("username", SIGN_IN_ENABLED_USERNAMES)
def test_accepted_users_reach_the_inventory(
    login_page: LoginPage, username: str
) -> None:
    """The site advertises six accounts; five of them must be able to sign in.

    Each behaves differently once signed in, so this covers the authentication
    boundary only: credentials are accepted and the catalogue is reachable.
    """
    login_page.login(username, PASSWORD)

    inventory_page = InventoryPage(login_page.page)

    inventory_page.expect_loaded()
    expect(inventory_page.page_title).to_have_text("Products")
    expect(inventory_page.inventory_items).to_have_count(6)


@allure.epic("Authentication")
@allure.feature("Sign in")
@allure.story("The login page advertises its accepted accounts")
@allure.severity(allure.severity_level.MINOR)
def test_login_page_lists_every_accepted_account(login_page: LoginPage) -> None:
    advertised = login_page.accepted_usernames

    expect(advertised).to_be_visible()
    for username in SIGN_IN_ENABLED_USERNAMES:
        expect(advertised).to_contain_text(username)
