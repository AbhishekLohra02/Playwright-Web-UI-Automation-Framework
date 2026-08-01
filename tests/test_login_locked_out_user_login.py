from playwright.sync_api import expect

from pages.login_page import LoginPage
from test_data.users import LOCKED_OUT_USERNAME, PASSWORD


def test_locked_out_user_login(
    login_page: LoginPage,
    base_url: str,
) -> None:
    login_page.login(LOCKED_OUT_USERNAME, PASSWORD)

    expect(login_page.page).to_have_url(base_url)
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_have_text(
        "Epic sadface: Sorry, this user has been locked out."
    )
