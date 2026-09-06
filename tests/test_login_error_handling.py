import allure
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.messages import INVALID_CREDENTIALS, USERNAME_REQUIRED
from test_data.users import (
    INVALID_PASSWORD,
    PASSWORD,
    STANDARD_USERNAME,
)

pytestmark = [pytest.mark.login, pytest.mark.regression]


@allure.epic("Authentication")
@allure.feature("Sign in")
@allure.story("A failed sign-in can be corrected without reloading")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.sanity
def test_error_can_be_dismissed_and_login_retried(
    login_page: LoginPage,
) -> None:
    """A user who mistypes a password must be able to recover in place."""
    login_page.login(STANDARD_USERNAME, INVALID_PASSWORD)

    expect(login_page.error_message).to_have_text(INVALID_CREDENTIALS)
    expect(login_page.username_input).to_have_class(
        f"{LoginPage.ERROR_INPUT_CLASS} form_input error"
    )

    login_page.dismiss_error()

    expect(login_page.error_message).to_have_count(0)
    expect(login_page.username_input).not_to_have_class(
        f"{LoginPage.ERROR_INPUT_CLASS} form_input error"
    )

    login_page.login(STANDARD_USERNAME, PASSWORD)

    expect(login_page.page).to_have_url("/inventory.html")


@allure.epic("Authentication")
@allure.feature("Sign in")
@allure.story("The form submits from the keyboard")
@allure.severity(allure.severity_level.NORMAL)
def test_login_can_be_submitted_with_the_enter_key(
    login_page: LoginPage,
) -> None:
    login_page.enter_credentials(STANDARD_USERNAME, PASSWORD)
    login_page.submit_with_enter()

    expect(login_page.page).to_have_url("/inventory.html")


@allure.epic("Authentication")
@allure.feature("Sign in")
@allure.story("Credentials are not exposed on screen")
@allure.severity(allure.severity_level.NORMAL)
def test_password_is_masked(login_page: LoginPage) -> None:
    expect(login_page.password_input).to_have_attribute("type", "password")


@allure.epic("Authentication")
@allure.feature("Sign in")
@allure.story("A rejected attempt does not carry over")
@allure.severity(allure.severity_level.MINOR)
def test_error_state_is_cleared_on_a_fresh_visit(
    login_page: LoginPage,
) -> None:
    login_page.login("", "")

    expect(login_page.error_message).to_have_text(USERNAME_REQUIRED)

    login_page.open()

    expect(login_page.error_message).to_have_count(0)
