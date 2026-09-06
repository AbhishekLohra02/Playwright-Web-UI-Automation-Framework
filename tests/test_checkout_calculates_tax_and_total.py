from decimal import ROUND_HALF_UP, Decimal

import allure
import pytest

from pages.checkout_overview_page import CheckoutOverviewPage

pytestmark = [pytest.mark.checkout, pytest.mark.regression]

TAX_RATE = Decimal("0.08")
CENTS = Decimal("0.01")


@allure.epic("Checkout")
@allure.feature("Order totals")
@allure.story("Tax and the payable total are correct")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.sanity
def test_checkout_calculates_tax_and_payable_total(
    checkout_overview_page: CheckoutOverviewPage,
) -> None:
    item_total = checkout_overview_page.displayed_item_total()
    tax = checkout_overview_page.displayed_tax()
    total = checkout_overview_page.displayed_total()

    expected_tax = (item_total * TAX_RATE).quantize(CENTS, rounding=ROUND_HALF_UP)

    assert tax == expected_tax
    assert total == item_total + tax
