from playwright.sync_api import Locator, Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_list = page.get_by_test_id("cart-list")
        self.cart_items = self.cart_list.get_by_test_id("inventory-item")

    def cart_item(self, product_name: str) -> Locator:
        return self.cart_items.filter(
            has=self.page.get_by_text(product_name, exact=True)
        )

