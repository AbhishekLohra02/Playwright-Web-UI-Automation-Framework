import allure
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from test_data.products import CART_PRODUCTS

pytestmark = [pytest.mark.cart, pytest.mark.regression]


@pytest.mark.manual_case("TC-CART-001", "TC-CART-003")
@allure.feature("Cart contents")
@allure.story("Selected products are retained")
@pytest.mark.smoke
@pytest.mark.sanity
def test_cart_retains_multiple_products(cart_with_products: CartPage) -> None:
    cart_with_products.expect_loaded()

    expect(cart_with_products.header.cart_badge).to_have_text(str(len(CART_PRODUCTS)))
    expect(cart_with_products.products.rows).to_have_count(len(CART_PRODUCTS))

    for product_name in CART_PRODUCTS:
        expect(cart_with_products.products.row(product_name)).to_be_visible()
