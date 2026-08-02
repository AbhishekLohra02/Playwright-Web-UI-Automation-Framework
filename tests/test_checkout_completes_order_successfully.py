from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_information_page import CheckoutInformationPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from test_data.customers import FIRST_NAME, LAST_NAME, POSTAL_CODE
from test_data.products import CART_PRODUCTS

def test_checkout_completes_order_successfully(
        logged_in_inventory_page: InventoryPage
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
    checkout_overview_page.finish_checkout()
    checkout_complete_page = CheckoutCompletePage(checkout_overview_page.page)
    expect(checkout_complete_page.complete_header).to_be_visible()
    expect(checkout_complete_page.complete_header).to_have_text("Thank you for your order!")
