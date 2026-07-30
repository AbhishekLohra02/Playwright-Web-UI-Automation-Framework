from playwright.sync_api import Page , expect
from pages.login_page import LoginPage
from test_data.users import STANDARD_USERNAME, PASSWORD
import pytest


@pytest.mark.parametrize(
        "username, password, expected_error",
        [
            pytest.param(
                "","","Epic sadface: Username is required"
            ),
            pytest.param(
                "",PASSWORD, "Epic sadface: Username is required"
            ),
            pytest.param(
                STANDARD_USERNAME, "", "Epic sadface: Password is required", 
            ),
        ],
)
def test_login_required_field_validation(
        page:Page,base_url:str, username:str, password:str,expected_error: str) -> None :
    
    login_page = LoginPage(page)
    login_page.open(base_url)
    login_page.login(username, password)

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_have_text(expected_error)
    