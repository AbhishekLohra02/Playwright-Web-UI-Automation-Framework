from playwright.sync_api import Page

from pages.base_page import AuthenticatedPage


class CheckoutCompletePage(AuthenticatedPage):
    url_path = "/checkout-complete.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.complete_header = page.get_by_test_id("complete-header")
        self.complete_text = page.get_by_test_id("complete-text")
        self.back_home_button = page.get_by_test_id("back-to-products")

    def back_home(self) -> None:
        self.back_home_button.click()
