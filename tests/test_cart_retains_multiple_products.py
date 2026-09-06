import allure
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from test_data.products import CART_PRODUCTS

pytestmark = [pytest.mark.cart, pytest.mark.regression]


@allure.epic("Shopping cart")
@allure.feature("Cart contents")
@allure.story("Selected products are retained")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
@pytest.mark.sanity
def test_cart_retains_multiple_products(cart_with_products: CartPage) -> None:
    cart_with_products.expect_loaded()

    expect(cart_with_products.cart_badge).to_have_text(str(len(CART_PRODUCTS)))
    expect(cart_with_products.cart_items).to_have_count(len(CART_PRODUCTS))

    for product_name in CART_PRODUCTS:
        expect(cart_with_products.cart_item(product_name)).to_be_visible()
