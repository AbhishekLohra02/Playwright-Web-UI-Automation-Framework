from decimal import Decimal
from playwright.sync_api import Page, Locator



class CheckoutOverviewPage:

    def __init__(self, page: Page):
        self.page = page
        self.checkout_list = page.get_by_test_id("cart-list")
        self.checkout_items = self.checkout_list.get_by_test_id("inventory-item")
        self.item_price_labels = self.checkout_items.get_by_test_id("inventory-item-price")
        self.item_total_label = page.get_by_test_id("subtotal-label")
        self.finish_button = page.get_by_role("button", name='Finish', exact=True)

    def checkout_item(self, product_name: str) -> Locator:
        return self.checkout_items.filter(
        has=self.page.get_by_text(product_name, exact=True)
    )

    def displayed_item_prices(self) -> list[Decimal]:
        price_texts = self.item_price_labels.all_inner_texts()
        for price_text in range(len(price_texts)):
            price_texts[price_text] = Decimal(price_texts[price_text].replace("$", "").strip())
        return price_texts
    
    def displayed_item_total(self) -> Decimal:
        total_text = self.item_total_label.inner_text()
        total_text = total_text.replace("Item total: $", "").strip()
        return Decimal(total_text)
    
    def finish_checkout(self) -> None:
        self.finish_button.click()
