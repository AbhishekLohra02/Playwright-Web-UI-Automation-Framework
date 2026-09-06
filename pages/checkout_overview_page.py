from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

import allure
from playwright.sync_api import Locator, Page, expect

from pages.base_page import AuthenticatedPage
from pages.components.product_collection import ProductCollection
from pages.prices import parse_price

if TYPE_CHECKING:
    from pages.checkout_complete_page import CheckoutCompletePage
    from pages.inventory_page import InventoryPage


class CheckoutOverviewPage(AuthenticatedPage):
    url_path = "/checkout-step-two.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.products = ProductCollection(page, page.get_by_test_id("cart-list"))
        self.item_total_label = page.get_by_test_id("subtotal-label")
        self.tax_label = page.get_by_test_id("tax-label")
        self.total_label = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_test_id("finish")
        self.cancel_button = page.get_by_test_id("cancel")

    def _amount(self, label: Locator) -> Decimal:
        expect(label).to_be_visible()
        return parse_price(label.inner_text())

    def displayed_item_total(self) -> Decimal:
        return self._amount(self.item_total_label)

    def displayed_tax(self) -> Decimal:
        return self._amount(self.tax_label)

    def displayed_total(self) -> Decimal:
        return self._amount(self.total_label)

    @allure.step("Finish the order")
    def finish_checkout(self) -> CheckoutCompletePage:
        from pages.checkout_complete_page import CheckoutCompletePage

        self.finish_button.click()

        complete_page = CheckoutCompletePage(self.page)
        complete_page.expect_loaded()
        return complete_page

    @allure.step("Cancel the order")
    def cancel_checkout(self) -> InventoryPage:
        from pages.inventory_page import InventoryPage

        self.cancel_button.click()

        inventory_page = InventoryPage(self.page)
        inventory_page.expect_loaded()
        return inventory_page
