import allure
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.messages import LOCKED_OUT_USER
from test_data.users import LOCKED_OUT_USERNAME, PASSWORD

pytestmark = [pytest.mark.login, pytest.mark.regression]


@allure.epic("Authentication")
@allure.feature("Sign in")
@allure.story("A locked-out account is refused")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.sanity
def test_locked_out_user_login(login_page: LoginPage) -> None:
    login_page.login(LOCKED_OUT_USERNAME, PASSWORD)

    login_page.expect_loaded()
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_have_text(LOCKED_OUT_USER)
