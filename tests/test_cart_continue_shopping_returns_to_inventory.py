import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from test_data.products import CART_PRODUCTS

pytestmark = [pytest.mark.cart, pytest.mark.regression]


def test_cart_continue_shopping_keeps_selected_products(
    cart_with_products: CartPage,
) -> None:
    cart_with_products.continue_shopping()

    inventory_page = InventoryPage(cart_with_products.page)

    inventory_page.expect_loaded()
    expect(inventory_page.cart_badge).to_have_text(str(len(CART_PRODUCTS)))
