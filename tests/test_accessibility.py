from collections.abc import Callable
from typing import Any

import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_information_page import CheckoutInformationPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = [pytest.mark.accessibility, pytest.mark.regression]

Scan = Callable[[str], list[dict[str, Any]]]


def _describe(violations: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"{violation['impact']}: {violation['id']} "
        f"({len(violation['nodes'])} node(s)) - {violation['help']}"
        for violation in violations
    )


@allure.feature("Accessibility")
@allure.story("The sign-in screen has no blocking accessibility defects")
@pytest.mark.manual_case("TC-UI-003", "TC-UI-005")
def test_login_page_has_no_blocking_accessibility_violations(
    login_page: LoginPage, accessibility_scan: Scan
) -> None:
    """Sign-in is the one screen nobody can route around.

    Critical and serious findings fail; moderate structural findings are
    attached to the report but do not block, because they do not stop anyone
    completing the journey.
    """
    violations = accessibility_scan("Login")

    assert not violations, _describe(violations)


@allure.feature("Accessibility")
@allure.story("The cart has no blocking accessibility defects")
@pytest.mark.manual_case("TC-UI-004")
def test_cart_page_has_no_blocking_accessibility_violations(
    cart_with_products: CartPage, accessibility_scan: Scan
) -> None:
    violations = accessibility_scan("Cart")

    assert not violations, _describe(violations)


@allure.feature("Accessibility")
@allure.story("Checkout has no blocking accessibility defects")
@pytest.mark.manual_case("TC-UI-005")
def test_checkout_information_has_no_blocking_accessibility_violations(
    checkout_information_page: CheckoutInformationPage, accessibility_scan: Scan
) -> None:
    violations = accessibility_scan("Checkout information")

    assert not violations, _describe(violations)


@allure.feature("Accessibility")
@allure.story("The catalogue has no blocking accessibility defects")
@pytest.mark.manual_case("TC-UI-004")
@pytest.mark.xfail(
    strict=True,
    reason=(
        "SD-007: the product sort dropdown has no accessible name, a critical "
        "axe-core `select-name` violation"
    ),
)
def test_inventory_page_has_no_blocking_accessibility_violations(
    logged_in_inventory_page: InventoryPage, accessibility_scan: Scan
) -> None:
    """The sort control is unusable with a screen reader.

    Marked strict so that adding a label upstream turns this green and tells us
    to drop the marker, rather than the defect quietly persisting.
    """
    violations = accessibility_scan("Inventory")

    assert not violations, _describe(violations)
