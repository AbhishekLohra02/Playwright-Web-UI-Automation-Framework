from decimal import Decimal

from playwright.sync_api import Locator, Page, expect

from pages.base_page import AuthenticatedPage
from pages.prices import parse_price


class CheckoutOverviewPage(AuthenticatedPage):
    url_path = "/checkout-step-two.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.checkout_list = page.get_by_test_id("cart-list")
        self.checkout_items = self.checkout_list.get_by_test_id("inventory-item")
        self.item_price_labels = self.checkout_items.get_by_test_id(
            "inventory-item-price"
        )
        self.item_total_label = page.get_by_test_id("subtotal-label")
        self.tax_label = page.get_by_test_id("tax-label")
        self.total_label = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_role("button", name="Finish", exact=True)
        self.cancel_button = page.get_by_role("button", name="Cancel", exact=True)

    def checkout_item(self, product_name: str) -> Locator:
        return self.checkout_items.filter(
            has=self.page.get_by_text(product_name, exact=True)
        )

    def displayed_item_prices(self) -> list[Decimal]:
        expect(self.item_price_labels.first).to_be_visible()
        return [parse_price(text) for text in self.item_price_labels.all_inner_texts()]

    def displayed_item_total(self) -> Decimal:
        expect(self.item_total_label).to_be_visible()
        return parse_price(self.item_total_label.inner_text())

    def displayed_tax(self) -> Decimal:
        expect(self.tax_label).to_be_visible()
        return parse_price(self.tax_label.inner_text())

    def displayed_total(self) -> Decimal:
        expect(self.total_label).to_be_visible()
        return parse_price(self.total_label.inner_text())

    def finish_checkout(self) -> None:
        self.finish_button.click()

    def cancel_checkout(self) -> None:
        self.cancel_button.click()
