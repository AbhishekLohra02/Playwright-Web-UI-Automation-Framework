import allure
import pytest
from playwright.sync_api import expect

from pages.checkout_information_page import CheckoutInformationPage
from pages.checkout_overview_page import CheckoutOverviewPage
from test_data.products import CART_PRODUCTS

pytestmark = [pytest.mark.checkout, pytest.mark.regression]


@pytest.mark.manual_case("TC-CHK-009")
@allure.feature("Abandoning an order")
@allure.story("Cancelling from the overview keeps the cart")
@pytest.mark.sanity
def test_cancel_from_the_order_overview_keeps_the_cart(
    checkout_overview_page: CheckoutOverviewPage,
) -> None:
    """A customer who backs out at the last step must not lose their basket.

    Silently emptying the cart on cancel would cost the sale outright, which
    makes this a revenue check rather than a navigation one.
    """
    inventory_page = checkout_overview_page.cancel_checkout()

    expect(inventory_page.header.cart_badge).to_have_text(str(len(CART_PRODUCTS)))


@pytest.mark.manual_case("TC-CHK-009")
@allure.feature("Abandoning an order")
@allure.story("Cancelling customer information returns to the cart")
def test_cancel_from_customer_information_returns_to_the_cart(
    checkout_information_page: CheckoutInformationPage,
) -> None:
    cart_page = checkout_information_page.cancel_checkout()

    expect(cart_page.products.rows).to_have_count(len(CART_PRODUCTS))
