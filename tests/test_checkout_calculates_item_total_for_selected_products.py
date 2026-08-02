from decimal import Decimal

from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_information_page import CheckoutInformationPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from test_data.customers import FIRST_NAME, LAST_NAME, POSTAL_CODE
from test_data.products import CART_PRODUCTS

def test_checkout_calculates_item_total_for_selected_products(
    logged_in_inventory_page: InventoryPage,
) -> None:
    for product_name in CART_PRODUCTS:
        logged_in_inventory_page.add_product_to_cart(product_name)

    logged_in_inventory_page.open_cart()
    cart_page = CartPage(logged_in_inventory_page.page)
    cart_page.start_checkout()

    checkout_information_page = CheckoutInformationPage(cart_page.page)
    checkout_information_page.enter_details(
        FIRST_NAME, LAST_NAME, POSTAL_CODE
    )
    checkout_information_page.click_continue()
    checkout_overview_page = CheckoutOverviewPage(checkout_information_page.page)

    expect(checkout_overview_page.checkout_items).to_have_count(len(CART_PRODUCTS))
    displayed_item_prices = checkout_overview_page.displayed_item_prices()
    displayed_item_total = checkout_overview_page.displayed_item_total()
    
    assert displayed_item_total == sum(displayed_item_prices)


