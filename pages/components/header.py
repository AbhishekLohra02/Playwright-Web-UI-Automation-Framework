from __future__ import annotations

from typing import TYPE_CHECKING

import allure
from playwright.sync_api import Page

if TYPE_CHECKING:
    from pages.cart_page import CartPage
    from pages.login_page import LoginPage


class HeaderComponent:
    """The banner and menu shared by every signed-in screen.

    Modelled as a component rather than a base class: a cart page is not a kind
    of header, it *has* one. Composition keeps these locators in one file, and
    keeps the page hierarchy describing pages rather than accumulating widgets.
    """

    def __init__(self, page: Page):
        self.page = page
        self.title = page.get_by_test_id("title")
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.menu_button = page.get_by_role("button", name="Open Menu")
        self.logout_link = page.get_by_test_id("logout-sidebar-link")
        self.reset_link = page.get_by_test_id("reset-sidebar-link")
        self.all_items_link = page.get_by_test_id("inventory-sidebar-link")

    @allure.step("Open the navigation menu")
    def open_menu(self) -> None:
        self.menu_button.click()

    @allure.step("Open the shopping cart")
    def open_cart(self) -> CartPage:
        from pages.cart_page import CartPage

        self.cart_link.click()
        return CartPage(self.page)

    @allure.step("Log out")
    def logout(self) -> LoginPage:
        from pages.login_page import LoginPage

        self.open_menu()
        self.logout_link.click()
        return LoginPage(self.page)

    @allure.step("Reset the application state")
    def reset_app_state(self) -> None:
        self.open_menu()
        self.reset_link.click()
