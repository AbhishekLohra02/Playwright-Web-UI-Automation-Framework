import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from test_data.products import BACKPACK, BIKE_LIGHT, CART_PRODUCTS

pytestmark = [pytest.mark.cart, pytest.mark.regression]

REMAINING_PRODUCTS = len(CART_PRODUCTS) - 1


@pytest.mark.sanity
def test_cart_removes_selected_product(cart_with_products: CartPage) -> None:
    expect(cart_with_products.cart_items).to_have_count(len(CART_PRODUCTS))

    cart_with_products.remove_product(BACKPACK)

    expect(cart_with_products.cart_items).to_have_count(REMAINING_PRODUCTS)
    expect(cart_with_products.cart_item(BACKPACK)).to_have_count(0)
    expect(cart_with_products.cart_item(BIKE_LIGHT)).to_be_visible()
    expect(cart_with_products.cart_badge).to_have_text(str(REMAINING_PRODUCTS))
