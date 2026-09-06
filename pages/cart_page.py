from playwright.sync_api import Locator, Page

from pages.base_page import AuthenticatedPage


class CartPage(AuthenticatedPage):
    url_path = "/cart.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_list = page.get_by_test_id("cart-list")
        self.cart_items = self.cart_list.get_by_test_id("inventory-item")
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.continue_shopping_button = page.get_by_test_id("continue-shopping")

    def cart_item(self, product_name: str) -> Locator:
        return self.cart_items.filter(
            has=self.page.get_by_text(product_name, exact=True)
        )

    def remove_product(self, product_name: str) -> None:
        self.cart_item(product_name).get_by_role(
            "button", name="Remove", exact=True
        ).click()

    def start_checkout(self) -> None:
        self.checkout_button.click()

    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()
