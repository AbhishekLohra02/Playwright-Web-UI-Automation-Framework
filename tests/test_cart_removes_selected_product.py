from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from test_data.products import BACKPACK, BIKE_LIGHT, CART_PRODUCTS


def test_cart_removes_selected_product(
    logged_in_inventory_page: InventoryPage,
) -> None:
    for product_name in CART_PRODUCTS:
        logged_in_inventory_page.add_product_to_cart(product_name)

    logged_in_inventory_page.open_cart()
    cart_page = CartPage(logged_in_inventory_page.page)

    expect(cart_page.cart_items).to_have_count(len(CART_PRODUCTS))

    cart_page.remove_product(BACKPACK)

    expect(cart_page.cart_items).to_have_count(len(CART_PRODUCTS) - 1)
    expect(cart_page.cart_item(BACKPACK)).to_have_count(0)
    expect(cart_page.cart_item(BIKE_LIGHT)).to_be_visible()
