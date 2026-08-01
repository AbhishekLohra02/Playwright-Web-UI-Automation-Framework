from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from test_data.products import CART_PRODUCTS


def test_cart_retains_multiple_products(
    logged_in_inventory_page: InventoryPage,
) -> None:
    for product_name in CART_PRODUCTS:
        logged_in_inventory_page.add_product_to_cart(product_name)

    expect(logged_in_inventory_page.cart_badge).to_have_text(
        str(len(CART_PRODUCTS))
    )

    logged_in_inventory_page.open_cart()
    cart_page = CartPage(logged_in_inventory_page.page)

    expect(cart_page.cart_items).to_have_count(len(CART_PRODUCTS))

    for product_name in CART_PRODUCTS:
        expect(cart_page.cart_item(product_name)).to_be_visible()
