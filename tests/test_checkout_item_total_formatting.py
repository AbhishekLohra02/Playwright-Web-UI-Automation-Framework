import re

import allure
import pytest
from playwright.sync_api import expect

from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from test_data.customers import FIRST_NAME, LAST_NAME, POSTAL_CODE
from test_data.products import CART_PRODUCTS, FLOAT_ARTIFACT_PRODUCTS

pytestmark = [pytest.mark.checkout, pytest.mark.regression]

# A currency amount: exactly two decimal places, never a raw float.
ITEM_TOTAL_CURRENCY = re.compile(r"^Item total: \$\d+\.\d{2}$")


def _reach_overview(
    inventory_page: InventoryPage, products: tuple[str, ...]
) -> CheckoutOverviewPage:
    for product_name in products:
        inventory_page.add_product_to_cart(product_name)

    information_page = inventory_page.header.open_cart().start_checkout()
    information_page.enter_details(FIRST_NAME, LAST_NAME, POSTAL_CODE)
    return information_page.continue_to_overview()


@pytest.mark.manual_case("TC-OVR-003")
@allure.feature("Order totals")
@allure.story("The item total is displayed as a currency amount")
@pytest.mark.sanity
def test_item_total_is_formatted_as_currency(
    checkout_overview_page: CheckoutOverviewPage,
) -> None:
    """Assert the format, not only the arithmetic.

    An arithmetic check compares one number against another and passes happily
    on `$105.96000000000001`-style output whenever the selected products happen
    to sum cleanly. Checking the rendered string catches the presentation
    defect regardless of which products were chosen.
    """
    expect(checkout_overview_page.item_total_label).to_have_text(ITEM_TOTAL_CURRENCY)


@pytest.mark.manual_case("TC-OVR-001", "TC-OVR-008")
@allure.feature("Order totals")
@allure.story("Every selected product is listed on the order overview")
def test_order_overview_lists_every_selected_product(
    checkout_overview_page: CheckoutOverviewPage,
) -> None:
    for product_name in CART_PRODUCTS:
        expect(checkout_overview_page.products.row(product_name)).to_be_visible()


@allure.feature("Order totals")
@allure.story("The item total is displayed as a currency amount")
@pytest.mark.xfail(
    strict=True,
    reason=(
        "SD-001: the order overview prints the item total as a raw "
        "floating-point value, for example $105.96000000000001"
    ),
)
def test_item_total_is_formatted_as_currency_for_a_lossy_price_sum(
    logged_in_inventory_page: InventoryPage,
) -> None:
    """Pin SD-001 to a product combination that reproduces it.

    Marked strict, so if SauceDemo ever rounds the subtotal correctly this test
    starts passing and the suite fails, telling us the defect is fixed and the
    marker should be removed.
    """
    overview_page = _reach_overview(logged_in_inventory_page, FLOAT_ARTIFACT_PRODUCTS)

    expect(overview_page.item_total_label).to_have_text(ITEM_TOTAL_CURRENCY)
