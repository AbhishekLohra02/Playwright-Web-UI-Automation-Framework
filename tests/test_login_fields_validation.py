import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.messages import PASSWORD_REQUIRED, USERNAME_REQUIRED
from test_data.users import PASSWORD, STANDARD_USERNAME

pytestmark = [pytest.mark.login, pytest.mark.regression]


@pytest.mark.sanity
@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        pytest.param("", "", USERNAME_REQUIRED, id="both_empty"),
        pytest.param("", PASSWORD, USERNAME_REQUIRED, id="username_empty"),
        pytest.param(STANDARD_USERNAME, "", PASSWORD_REQUIRED, id="password_empty"),
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
