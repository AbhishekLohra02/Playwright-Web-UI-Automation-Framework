import allure
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from test_data.products import CART_PRODUCTS

pytestmark = [pytest.mark.cart, pytest.mark.regression]


@pytest.mark.manual_case("TC-CART-006")
@allure.feature("Navigation")
@allure.story("Continue shopping preserves the cart")
def test_cart_continue_shopping_keeps_selected_products(
    cart_with_products: CartPage,
) -> None:
    inventory_page = cart_with_products.continue_shopping()

    expect(inventory_page.header.cart_badge).to_have_text(str(len(CART_PRODUCTS)))
