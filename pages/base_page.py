import allure
from playwright.sync_api import Page, expect


class BasePage:
    """Common behavior shared by every SauceDemo page object.

    Subclasses declare the path they own so that navigation and page-state
    checks are expressed once instead of being rebuilt in each test.
    """

    url_path = "/"

    def __init__(self, page: Page):
        self.page = page

    def open(self) -> None:
        with allure.step(f"Open {self.url_path}"):
            self.page.goto(self.url_path)

    def expect_loaded(self) -> None:
        with allure.step(f"Wait for {self.url_path}"):
            expect(self.page).to_have_url(self.url_path)


class AuthenticatedPage(BasePage):
    """Pages shown after login, which all share the same header and menu."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_title = page.get_by_test_id("title")
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.menu_button = page.get_by_role("button", name="Open Menu")
        self.logout_link = page.get_by_test_id("logout-sidebar-link")
        self.reset_link = page.get_by_test_id("reset-sidebar-link")

    @allure.step("Open the shopping cart")
    def open_cart(self) -> None:
        self.cart_link.click()

    @allure.step("Log out")
    def logout(self) -> None:
        self.menu_button.click()
        self.logout_link.click()

    @allure.step("Reset the application state")
    def reset_app_state(self) -> None:
        self.menu_button.click()
        self.reset_link.click()
