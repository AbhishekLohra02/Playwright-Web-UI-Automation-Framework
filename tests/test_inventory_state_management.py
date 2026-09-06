import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from test_data.products import BACKPACK, CART_PRODUCTS

pytestmark = [pytest.mark.inventory, pytest.mark.regression]


@allure.feature("Cart state")
@allure.story("A product can be removed from the catalogue listing")
@pytest.mark.sanity
def test_product_can_be_removed_without_opening_the_cart(
    logged_in_inventory_page: InventoryPage,
) -> None:
    """The catalogue's own Remove button is a separate control from the cart's."""
    logged_in_inventory_page.add_product_to_cart(BACKPACK)

    expect(logged_in_inventory_page.header.cart_badge).to_have_text("1")

    logged_in_inventory_page.remove_product_from_cart(BACKPACK)

    expect(logged_in_inventory_page.header.cart_badge).to_have_count(0)
    expect(
        logged_in_inventory_page.products.row(BACKPACK).get_by_role("button")
    ).to_have_text("Add to cart")


@allure.feature("Cart state")
@allure.story("Reset App State empties the cart")
def test_reset_app_state_empties_the_cart(
    logged_in_inventory_page: InventoryPage,
) -> None:
    for product_name in CART_PRODUCTS:
        logged_in_inventory_page.add_product_to_cart(product_name)

    expect(logged_in_inventory_page.header.cart_badge).to_have_text(
        str(len(CART_PRODUCTS))
    )

    logged_in_inventory_page.header.reset_app_state()

    expect(logged_in_inventory_page.header.cart_badge).to_have_count(0)


@allure.feature("Cart state")
@allure.story("Reset App State refreshes the catalogue buttons")
@pytest.mark.xfail(
    strict=True,
    reason=(
        "SD-006: Reset App State clears the cart but leaves the catalogue "
        "buttons reading 'Remove' until the page is reloaded"
    ),
)
def test_reset_app_state_restores_the_add_to_cart_buttons(
    logged_in_inventory_page: InventoryPage,
) -> None:
    """The reset leaves the page contradicting itself.

    The badge and the cart are cleared, but every button a customer can see
    still offers to remove a product that is no longer in their cart. Marked
    strict so a fix upstream is noticed rather than silently absorbed.
    """
    logged_in_inventory_page.add_product_to_cart(BACKPACK)
    logged_in_inventory_page.header.reset_app_state()

    expect(
        logged_in_inventory_page.products.row(BACKPACK).get_by_role("button")
    ).to_have_text("Add to cart")
