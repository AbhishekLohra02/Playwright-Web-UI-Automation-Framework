from playwright.sync_api import Page


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.page_title = page.get_by_test_id("title")
        self.inventory_list = page.get_by_test_id("inventory-list")
        self.inventory_items = self.inventory_list.get_by_test_id(
            "inventory-item"
        )
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")

    def add_product_to_cart(self, product_name: str) -> None:
        product_card = self.inventory_items.filter(
            has=self.page.get_by_text(product_name, exact=True)
        )
        product_card.get_by_role("button", name="Add to cart").click()

    def open_cart(self) -> None:
        self.cart_link.click()
