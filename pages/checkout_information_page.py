from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from playwright.sync_api import Page

from pages.base_page import AuthenticatedPage

if TYPE_CHECKING:
    from pages.cart_page import CartPage
    from pages.checkout_overview_page import CheckoutOverviewPage


class CheckoutInformationPage(AuthenticatedPage):
    url_path = "/checkout-step-one.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.postal_code_input = page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.cancel_button = page.get_by_test_id("cancel")
        self.error_message = page.get_by_test_id("error")

    @allure.step("Enter customer information")
    def enter_details(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    @allure.step("Submit the customer information form")
    def click_continue(self) -> None:
        """Submit without asserting where it leads.

        Required-field tests expect to stay on this page, so this variant makes
        no promise about the next screen.
        """
        self.continue_button.click()

    @allure.step("Continue to the order overview")
    def continue_to_overview(self) -> CheckoutOverviewPage:
        from pages.checkout_overview_page import CheckoutOverviewPage

        self.click_continue()

        overview_page = CheckoutOverviewPage(self.page)
        overview_page.expect_loaded()
        return overview_page

    @allure.step("Cancel the checkout")
    def cancel_checkout(self) -> CartPage:
        from pages.cart_page import CartPage

        self.cancel_button.click()

        cart_page = CartPage(self.page)
        cart_page.expect_loaded()
        return cart_page
