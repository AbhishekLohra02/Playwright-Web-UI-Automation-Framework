from __future__ import annotations

import re
from decimal import Decimal
from typing import TYPE_CHECKING

import allure
from playwright.sync_api import Page, expect

from pages.base_page import AuthenticatedPage
from pages.prices import parse_price

if TYPE_CHECKING:
    from pages.inventory_page import InventoryPage


class ProductDetailPage(AuthenticatedPage):
    """A single product's page, reached by clicking a product name.

    The path carries a product id, so this page identifies itself by pattern
    rather than by the fixed `url_path` the other screens use.
    """

    url_path = "/inventory-item.html"
    URL_PATTERN = re.compile(r"/inventory-item\.html\?id=\d+$")

    def __init__(self, page: Page):
        super().__init__(page)
        self.product_name = page.get_by_test_id("inventory-item-name")
        self.product_description = page.get_by_test_id("inventory-item-desc")
        self.product_price = page.get_by_test_id("inventory-item-price")
        self.product_image = page.locator(".inventory_details_img")
        self.add_to_cart_button = page.get_by_test_id("add-to-cart")
        self.remove_button = page.get_by_test_id("remove")
        self.back_to_products_button = page.get_by_test_id("back-to-products")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(self.URL_PATTERN)

    def displayed_price(self) -> Decimal:
        expect(self.product_price).to_be_visible()
        return parse_price(self.product_price.inner_text())

    @allure.step("Add the displayed product to the cart")
    def add_to_cart(self) -> None:
        self.add_to_cart_button.click()

    @allure.step("Remove the displayed product from the cart")
    def remove_from_cart(self) -> None:
        self.remove_button.click()

    @allure.step("Go back to the product catalogue")
    def back_to_products(self) -> InventoryPage:
        from pages.inventory_page import InventoryPage

        self.back_to_products_button.click()

        inventory_page = InventoryPage(self.page)
        inventory_page.expect_loaded()
        return inventory_page
