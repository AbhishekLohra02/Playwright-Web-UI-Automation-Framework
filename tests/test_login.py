import allure
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.users import PASSWORD, STANDARD_USERNAME

pytestmark = [pytest.mark.login, pytest.mark.regression]


@pytest.mark.manual_case("TC-AUTH-001")
@allure.feature("Sign in")
@allure.story("The standard account reaches the catalogue")
@pytest.mark.smoke
@pytest.mark.sanity
def test_successful_login_with_standard_user(login_page: LoginPage) -> None:
    inventory_page = login_page.login_as(STANDARD_USERNAME, PASSWORD)

    expect(inventory_page.header.title).to_be_visible()
    expect(inventory_page.header.title).to_have_text("Products")
