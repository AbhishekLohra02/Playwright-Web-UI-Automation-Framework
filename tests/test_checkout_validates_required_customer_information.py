import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_information_page import CheckoutInformationPage
from pages.inventory_page import InventoryPage
from test_data.customers import FIRST_NAME, LAST_NAME, POSTAL_CODE
from test_data.products import BACKPACK


@pytest.mark.parametrize(
    "first_name, last_name, postal_code, expected_error",
    [
        (
            "",
            LAST_NAME,
            POSTAL_CODE,
            "Error: First Name is required",
        ),
        (
            FIRST_NAME,
            "",
            POSTAL_CODE,
            "Error: Last Name is required",
        ),
        (
            FIRST_NAME,
            LAST_NAME,
            "",
            "Error: Postal Code is required",
        ),
    ],
)
def test_checkout_validates_required_customer_information(
    logged_in_inventory_page: InventoryPage,
    first_name: str,
    last_name: str,
    postal_code: str,
    expected_error: str,
) -> None:
    logged_in_inventory_page.add_product_to_cart(BACKPACK)
    logged_in_inventory_page.open_cart()

    cart_page = CartPage(logged_in_inventory_page.page)
    cart_page.start_checkout()

    checkout_information_page = CheckoutInformationPage(cart_page.page)
    checkout_information_page.enter_details(
        first_name,
        last_name,
        postal_code,
    )
    checkout_information_page.click_continue()

    expect(checkout_information_page.error_message).to_be_visible()
    expect(checkout_information_page.error_message).to_have_text(
        expected_error
    )
