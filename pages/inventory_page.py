from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from playwright.sync_api import Page

from pages.base_page import AuthenticatedPage
from pages.components.product_collection import ProductCollection

if TYPE_CHECKING:
    from pages.product_detail_page import ProductDetailPage


class InventoryPage(AuthenticatedPage):
    url_path = "/inventory.html"

    PRICE_LOW_TO_HIGH = "Price (low to high)"
    PRICE_HIGH_TO_LOW = "Price (high to low)"
    NAME_A_TO_Z = "Name (A to Z)"
    NAME_Z_TO_A = "Name (Z to A)"

    def __init__(self, page: Page):
        super().__init__(page)
        self.products = ProductCollection(page, page.get_by_test_id("inventory-list"))
        self.sort_dropdown = page.get_by_test_id("product-sort-container")

    @allure.step("Add '{product_name}' to the cart")
    def add_product_to_cart(self, product_name: str) -> None:
        self.products.row(product_name).get_by_role(
            "button", name="Add to cart"
        ).click()

    @allure.step("Remove '{product_name}' from the cart")
    def remove_product_from_cart(self, product_name: str) -> None:
        self.products.row(product_name).get_by_role(
            "button", name="Remove", exact=True
        ).click()

    @allure.step("Open the detail page for '{product_name}'")
    def open_product_detail(self, product_name: str) -> ProductDetailPage:
        from pages.product_detail_page import ProductDetailPage

        self.products.row(product_name).get_by_text(product_name, exact=True).click()

        detail_page = ProductDetailPage(self.page)
        detail_page.expect_loaded()
        return detail_page

    @allure.step("Sort products by '{option_label}'")
    def sort_products_by(self, option_label: str) -> None:
        self.sort_dropdown.select_option(label=option_label)
