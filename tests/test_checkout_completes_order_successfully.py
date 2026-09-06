import allure
import pytest
from playwright.sync_api import expect

from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from test_data.messages import ORDER_COMPLETE_HEADER, ORDER_COMPLETE_TEXT

pytestmark = [pytest.mark.checkout, pytest.mark.regression]


@allure.epic("Checkout")
@allure.feature("Order completion")
@allure.story("An order can be placed end to end")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
@pytest.mark.sanity
def test_checkout_completes_order_successfully(
    checkout_overview_page: CheckoutOverviewPage,
) -> None:
    checkout_overview_page.finish_checkout()

    checkout_complete_page = CheckoutCompletePage(checkout_overview_page.page)

    checkout_complete_page.expect_loaded()
    expect(checkout_complete_page.complete_header).to_be_visible()
    expect(checkout_complete_page.complete_header).to_have_text(ORDER_COMPLETE_HEADER)
    expect(checkout_complete_page.complete_text).to_have_text(ORDER_COMPLETE_TEXT)


@allure.epic("Checkout")
@allure.feature("Order completion")
@allure.story("A completed order empties the cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.sanity
def test_completed_order_empties_the_cart(
    checkout_overview_page: CheckoutOverviewPage,
) -> None:
    checkout_overview_page.finish_checkout()

    checkout_complete_page = CheckoutCompletePage(checkout_overview_page.page)
    checkout_complete_page.expect_loaded()

    expect(checkout_complete_page.cart_badge).to_have_count(0)

    checkout_complete_page.back_home()

    inventory_page = InventoryPage(checkout_complete_page.page)

    inventory_page.expect_loaded()
    expect(inventory_page.cart_badge).to_have_count(0)
