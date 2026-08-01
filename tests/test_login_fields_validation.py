import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.users import PASSWORD, STANDARD_USERNAME


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        pytest.param("", "", "Epic sadface: Username is required"),
        pytest.param(
            "",
            PASSWORD,
            "Epic sadface: Username is required",
        ),
        pytest.param(
            STANDARD_USERNAME,
            "",
            "Epic sadface: Password is required",
        ),
    ],
)
def test_login_required_field_validation(
    login_page: LoginPage,
    username: str,
    password: str,
    expected_error: str,
) -> None:
    login_page.login(username, password)

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_have_text(expected_error)
