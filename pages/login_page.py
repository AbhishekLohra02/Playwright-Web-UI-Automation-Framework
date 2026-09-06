import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    url_path = "/"

    ERROR_INPUT_CLASS = "input_error"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.get_by_test_id("error")
        self.error_close_button = page.get_by_test_id("error-button")
        self.accepted_usernames = page.locator("#login_credentials")

    @allure.step("Log in as '{username}'")
    def login(self, username: str, password: str) -> None:
        self.enter_credentials(username, password)
        self.login_button.click()

    def enter_credentials(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)

    @allure.step("Submit the login form with the Enter key")
    def submit_with_enter(self) -> None:
        self.password_input.press("Enter")

    @allure.step("Dismiss the login error message")
    def dismiss_error(self) -> None:
        self.error_close_button.click()
