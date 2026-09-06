from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from playwright.sync_api import Page

from pages.base_page import AuthenticatedPage

if TYPE_CHECKING:
    from pages.inventory_page import InventoryPage


class CheckoutCompletePage(AuthenticatedPage):
    url_path = "/checkout-complete.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.complete_header = page.get_by_test_id("complete-header")
        self.complete_text = page.get_by_test_id("complete-text")
        self.back_home_button = page.get_by_test_id("back-to-products")

    @allure.step("Return to the product catalogue")
    def back_home(self) -> InventoryPage:
        from pages.inventory_page import InventoryPage

        self.back_home_button.click()

        inventory_page = InventoryPage(self.page)
        inventory_page.expect_loaded()
        return inventory_page
