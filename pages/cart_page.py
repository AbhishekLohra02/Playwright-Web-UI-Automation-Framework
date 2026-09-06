from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from playwright.sync_api import Page

from pages.base_page import AuthenticatedPage
from pages.components.product_collection import ProductCollection

if TYPE_CHECKING:
    from pages.checkout_information_page import CheckoutInformationPage
    from pages.inventory_page import InventoryPage


class CartPage(AuthenticatedPage):
    url_path = "/cart.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.products = ProductCollection(page, page.get_by_test_id("cart-list"))
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.continue_shopping_button = page.get_by_test_id("continue-shopping")

    @allure.step("Remove '{product_name}' from the cart")
    def remove_product(self, product_name: str) -> None:
        self.products.row(product_name).get_by_role(
            "button", name="Remove", exact=True
        ).click()

    @allure.step("Start checkout")
    def start_checkout(self) -> CheckoutInformationPage:
        from pages.checkout_information_page import CheckoutInformationPage

        self.checkout_button.click()

        information_page = CheckoutInformationPage(self.page)
        information_page.expect_loaded()
        return information_page

    @allure.step("Continue shopping")
    def continue_shopping(self) -> InventoryPage:
        from pages.inventory_page import InventoryPage

        self.continue_shopping_button.click()

        inventory_page = InventoryPage(self.page)
        inventory_page.expect_loaded()
        return inventory_page
