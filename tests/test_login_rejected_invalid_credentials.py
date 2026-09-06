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


@pytest.mark.parametrize(
    ("username", "password"),
    [
        pytest.param(UNKNOWN_USERNAME, PASSWORD, id="unknown_username"),
        pytest.param(STANDARD_USERNAME, INVALID_PASSWORD, id="wrong_password"),
        pytest.param(UNKNOWN_USERNAME, INVALID_PASSWORD, id="both_invalid"),
    ],
)
def test_login_invalid_credentials(
    login_page: LoginPage,
    username: str,
    password: str,
) -> None:
    login_page.login(username, password)

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_have_text(INVALID_CREDENTIALS)
    login_page.expect_loaded()
