import allure
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.users import PASSWORD, SIGN_IN_ENABLED_USERNAMES

pytestmark = [pytest.mark.login, pytest.mark.regression]


@pytest.mark.manual_case("TC-INV-001", "TC-INV-002")
@allure.feature("Sign in")
@allure.story("Every advertised account reaches the catalogue")
@pytest.mark.sanity
@pytest.mark.parametrize("username", SIGN_IN_ENABLED_USERNAMES)
def test_accepted_users_reach_the_inventory(
    login_page: LoginPage, username: str
) -> None:
    """The site advertises six accounts; five of them must be able to sign in.

    Each behaves differently once signed in, so this covers the authentication
    boundary only: credentials are accepted and the catalogue is reachable.
    """
    inventory_page = login_page.login_as(username, PASSWORD)

    expect(inventory_page.header.title).to_have_text("Products")
    expect(inventory_page.products.rows).to_have_count(6)


@allure.feature("Sign in")
@allure.story("The login page advertises its accepted accounts")
def test_login_page_lists_every_accepted_account(login_page: LoginPage) -> None:
    advertised = login_page.accepted_usernames

    expect(advertised).to_be_visible()
    for username in SIGN_IN_ENABLED_USERNAMES:
        expect(advertised).to_contain_text(username)
