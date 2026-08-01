import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.users import (
    INVALID_PASSWORD,
    PASSWORD,
    STANDARD_USERNAME,
    UNKNOWN_USERNAME,
)


@pytest.mark.parametrize(
    "username, password",
    [
        pytest.param(UNKNOWN_USERNAME, PASSWORD),
        pytest.param(STANDARD_USERNAME, INVALID_PASSWORD),
        pytest.param(UNKNOWN_USERNAME, INVALID_PASSWORD),
    ],
)
def test_login_invalid_credentials(
    login_page: LoginPage,
    base_url: str,
    username: str,
    password: str,
) -> None:
    login_page.login(username, password)

    expect(login_page.error_message).to_have_text(
        "Epic sadface: Username and password do not match any user in this service"
    )
    expect(login_page.page).to_have_url(base_url)
    expect(login_page.error_message).to_be_visible()

