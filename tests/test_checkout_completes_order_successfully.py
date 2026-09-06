import allure
import pytest
from playwright.sync_api import expect

from pages.checkout_overview_page import CheckoutOverviewPage
from test_data.messages import ORDER_COMPLETE_HEADER, ORDER_COMPLETE_TEXT

pytestmark = [pytest.mark.checkout, pytest.mark.regression]


@allure.feature("Order completion")
@allure.story("An order can be placed end to end")
@pytest.mark.smoke
@pytest.mark.sanity
def test_checkout_completes_order_successfully(
    checkout_overview_page: CheckoutOverviewPage,
) -> None:
    checkout_complete_page = checkout_overview_page.finish_checkout()

    expect(checkout_complete_page.complete_header).to_be_visible()
    expect(checkout_complete_page.complete_header).to_have_text(ORDER_COMPLETE_HEADER)
    expect(checkout_complete_page.complete_text).to_have_text(ORDER_COMPLETE_TEXT)


@allure.feature("Order completion")
@allure.story("A completed order empties the cart")
@pytest.mark.sanity
def test_completed_order_empties_the_cart(
    checkout_overview_page: CheckoutOverviewPage,
) -> None:
    checkout_complete_page = checkout_overview_page.finish_checkout()

    expect(checkout_complete_page.header.cart_badge).to_have_count(0)

    inventory_page = checkout_complete_page.back_home()

    expect(inventory_page.header.cart_badge).to_have_count(0)
