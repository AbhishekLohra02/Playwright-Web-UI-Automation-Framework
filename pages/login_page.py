from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.inventory_page import InventoryPage


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

    def enter_credentials(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)

    @allure.step("Submit the login form as '{username}'")
    def login(self, username: str, password: str) -> None:
        """Submit credentials without asserting where they lead.

        Negative tests use this: they expect to stay on the login page, so
        promising a next page here would be a lie.
        """
        self.enter_credentials(username, password)
        self.login_button.click()

    @allure.step("Sign in as '{username}'")
    def login_as(self, username: str, password: str) -> InventoryPage:
        """Sign in and land on the catalogue.

        The happy path, and the only variant that may promise a next page.
        """
        from pages.inventory_page import InventoryPage

        self.login(username, password)

        inventory_page = InventoryPage(self.page)
        inventory_page.expect_loaded()
        return inventory_page

    @allure.step("Submit the login form with the Enter key")
    def submit_with_enter(self) -> None:
        self.password_input.press("Enter")

    @allure.step("Dismiss the login error message")
    def dismiss_error(self) -> None:
        self.error_close_button.click()
