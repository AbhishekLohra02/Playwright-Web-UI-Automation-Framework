import allure
import pytest
from playwright.sync_api import expect

from pages.checkout_overview_page import CheckoutOverviewPage
from test_data.products import CART_PRODUCTS

pytestmark = [pytest.mark.checkout, pytest.mark.regression]


@pytest.mark.manual_case("TC-OVR-003")
@allure.feature("Order totals")
@allure.story("The item total matches the selected products")
@pytest.mark.sanity
def test_checkout_calculates_item_total_for_selected_products(
    checkout_overview_page: CheckoutOverviewPage,
) -> None:
    checkout_overview_page.expect_loaded()
    expect(checkout_overview_page.products.rows).to_have_count(len(CART_PRODUCTS))

    displayed_item_prices = checkout_overview_page.products.prices()

    assert checkout_overview_page.displayed_item_total() == sum(displayed_item_prices)
