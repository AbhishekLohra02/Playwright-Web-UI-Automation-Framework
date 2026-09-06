import allure
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.messages import INVALID_CREDENTIALS
from test_data.users import (
    INVALID_PASSWORD,
    PASSWORD,
    STANDARD_USERNAME,
    UNKNOWN_USERNAME,
)

pytestmark = [pytest.mark.login, pytest.mark.regression]

REJECTED_CREDENTIALS = [
    pytest.param(UNKNOWN_USERNAME, PASSWORD, id="unknown_username"),
    pytest.param(STANDARD_USERNAME, INVALID_PASSWORD, id="wrong_password"),
    pytest.param(UNKNOWN_USERNAME, INVALID_PASSWORD, id="both_invalid"),
    pytest.param(STANDARD_USERNAME, "secret_sauc", id="password_off_by_one"),
    pytest.param("STANDARD_USER", PASSWORD, id="username_wrong_case"),
    pytest.param(STANDARD_USERNAME, "SECRET_SAUCE", id="password_wrong_case"),
    pytest.param(f" {STANDARD_USERNAME} ", PASSWORD, id="username_padded"),
    pytest.param(STANDARD_USERNAME, f" {PASSWORD}", id="password_padded"),
]

MALICIOUS_CREDENTIALS = [
    pytest.param("' OR '1'='1", "' OR '1'='1", id="sql_injection_attempt"),
    pytest.param("<script>alert(1)</script>", PASSWORD, id="script_injection"),
    pytest.param("a" * 300, "b" * 300, id="oversized_input"),
]


@allure.feature("Sign in")
@allure.story("Invalid credentials are rejected")
@pytest.mark.parametrize(("username", "password"), REJECTED_CREDENTIALS)
def test_login_rejects_invalid_credentials(
    login_page: LoginPage,
    username: str,
    password: str,
) -> None:
    """Credentials must match exactly.

    Case differences and surrounding whitespace are covered here because a
    permissive comparison is a real authentication weakness, not a cosmetic one.
    """
    login_page.login(username, password)

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_have_text(INVALID_CREDENTIALS)
    login_page.expect_loaded()


@allure.feature("Sign in")
@allure.story("Malicious input is rejected without leaking behavior")
@pytest.mark.parametrize(("username", "password"), MALICIOUS_CREDENTIALS)
def test_login_rejects_malicious_input(
    login_page: LoginPage,
    username: str,
    password: str,
) -> None:
    """Injection-style input is refused with the ordinary failure message.

    Returning the same generic error for hostile input matters twice over: it
    proves the payload was not interpreted, and it avoids telling an attacker
    that their input was treated as special.
    """
    login_page.login(username, password)

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_have_text(INVALID_CREDENTIALS)
    login_page.expect_loaded()
