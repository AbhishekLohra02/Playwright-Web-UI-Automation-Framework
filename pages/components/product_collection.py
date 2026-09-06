from decimal import Decimal

from playwright.sync_api import Locator, Page, expect

from pages.prices import parse_price


class ProductCollection:
    """A repeated list of product rows.

    The inventory grid, the cart list and the order overview all render the
    same row markup. Filtering a row by product name and reading its price were
    previously written out in three page objects; they live here once instead.

    Reads that leave Playwright's retrying world - `all_inner_texts()` returns
    a plain list - are guarded by an `expect()` first, so the collection cannot
    be read before it has rendered.
    """

    def __init__(self, page: Page, container: Locator):
        self.page = page
        self.rows = container.get_by_test_id("inventory-item")
        self.name_labels = self.rows.get_by_test_id("inventory-item-name")
        self.price_labels = self.rows.get_by_test_id("inventory-item-price")

    def row(self, product_name: str) -> Locator:
        """The single row for a product, matched on its exact visible name."""
        return self.rows.filter(has=self.page.get_by_text(product_name, exact=True))

    def button_for(self, product_name: str) -> Locator:
        """A row's action button, whose label flips between Add and Remove."""
        return self.row(product_name).get_by_role("button")

    def names(self) -> list[str]:
        expect(self.name_labels.first).to_be_visible()
        return self.name_labels.all_inner_texts()

    def prices(self) -> list[Decimal]:
        expect(self.price_labels.first).to_be_visible()
        return [parse_price(text) for text in self.price_labels.all_inner_texts()]
