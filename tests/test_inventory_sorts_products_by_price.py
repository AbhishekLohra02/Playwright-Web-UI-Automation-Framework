import allure
import pytest

from pages.inventory_page import InventoryPage

pytestmark = [pytest.mark.inventory, pytest.mark.regression]


@allure.feature("Sorting")
@allure.story("Products sort by ascending price")
@pytest.mark.sanity
def test_inventory_sorts_products_by_price_low_to_high(
    logged_in_inventory_page: InventoryPage,
) -> None:
    logged_in_inventory_page.sort_products_by(InventoryPage.PRICE_LOW_TO_HIGH)

    displayed_prices = logged_in_inventory_page.products.prices()

    assert displayed_prices == sorted(displayed_prices)


@allure.feature("Sorting")
@allure.story("Products sort by descending price")
@pytest.mark.sanity
def test_inventory_sorts_products_by_price_high_to_low(
    logged_in_inventory_page: InventoryPage,
) -> None:
    logged_in_inventory_page.sort_products_by(InventoryPage.PRICE_HIGH_TO_LOW)

    displayed_prices = logged_in_inventory_page.products.prices()

    assert displayed_prices == sorted(displayed_prices, reverse=True)


@allure.feature("Sorting")
@allure.story("Products sort by name")
@pytest.mark.sanity
def test_inventory_sorts_products_by_name(
    logged_in_inventory_page: InventoryPage,
) -> None:
    logged_in_inventory_page.sort_products_by(InventoryPage.NAME_Z_TO_A)

    displayed_names = logged_in_inventory_page.products.names()

    assert displayed_names == sorted(displayed_names, reverse=True)
