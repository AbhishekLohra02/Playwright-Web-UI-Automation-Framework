from decimal import Decimal

import allure
from playwright.sync_api import Locator, Page, expect

from pages.base_page import AuthenticatedPage
from pages.prices import parse_price


class InventoryPage(AuthenticatedPage):
    url_path = "/inventory.html"

    PRICE_LOW_TO_HIGH = "Price (low to high)"
    PRICE_HIGH_TO_LOW = "Price (high to low)"
    NAME_A_TO_Z = "Name (A to Z)"
    NAME_Z_TO_A = "Name (Z to A)"

    def __init__(self, page: Page):
        super().__init__(page)
        self.inventory_list = page.get_by_test_id("inventory-list")
        self.inventory_items = self.inventory_list.get_by_test_id("inventory-item")
        self.item_name_labels = self.inventory_items.get_by_test_id(
            "inventory-item-name"
        )
        self.item_price_labels = self.inventory_items.get_by_test_id(
            "inventory-item-price"
        )
        self.sort_dropdown = page.get_by_test_id("product-sort-container")

    def product_card(self, product_name: str) -> Locator:
        return self.inventory_items.filter(
            has=self.page.get_by_text(product_name, exact=True)
        )

    @allure.step("Add '{product_name}' to the cart")
    def add_product_to_cart(self, product_name: str) -> None:
        self.product_card(product_name).get_by_role(
            "button", name="Add to cart"
        ).click()

    @allure.step("Remove '{product_name}' from the cart")
    def remove_product_from_cart(self, product_name: str) -> None:
        self.product_card(product_name).get_by_role(
            "button", name="Remove", exact=True
        ).click()

    @allure.step("Sort products by '{option_label}'")
    def sort_products_by(self, option_label: str) -> None:
        self.sort_dropdown.select_option(label=option_label)

    def displayed_product_names(self) -> list[str]:
        expect(self.item_name_labels.first).to_be_visible()
        return self.item_name_labels.all_inner_texts()

    def displayed_product_prices(self) -> list[Decimal]:
        expect(self.item_price_labels.first).to_be_visible()
        return [parse_price(text) for text in self.item_price_labels.all_inner_texts()]
