import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from test_data.products import BACKPACK, CATALOGUE

pytestmark = [pytest.mark.inventory, pytest.mark.regression]


@pytest.mark.manual_case("TC-DET-001", "TC-DET-002", "TC-INV-006")
@allure.feature("Product detail")
@allure.story("A product's detail page matches the catalogue")
@pytest.mark.sanity
def test_product_detail_matches_the_catalogue_entry(
    logged_in_inventory_page: InventoryPage,
) -> None:
    """The detail page is where a customer decides to buy.

    A price that disagrees with the catalogue listing is a pricing defect, so
    the price is compared against the known catalogue value rather than against
    whatever the previous screen happened to show.
    """
    detail_page = logged_in_inventory_page.open_product_detail(BACKPACK)

    expect(detail_page.product_name).to_have_text(BACKPACK)
    expect(detail_page.product_description).not_to_be_empty()
    expect(detail_page.product_image).to_be_visible()

    assert detail_page.displayed_price() == CATALOGUE[BACKPACK]


@pytest.mark.manual_case("TC-DET-004")
@allure.feature("Product detail")
@allure.story("A product can be bought from its detail page")
@pytest.mark.sanity
def test_product_can_be_added_to_the_cart_from_its_detail_page(
    logged_in_inventory_page: InventoryPage,
) -> None:
    detail_page = logged_in_inventory_page.open_product_detail(BACKPACK)
    detail_page.add_to_cart()

    expect(detail_page.header.cart_badge).to_have_text("1")
    expect(detail_page.remove_button).to_be_visible()
    expect(detail_page.add_to_cart_button).to_have_count(0)


@pytest.mark.manual_case("TC-DET-007")
@allure.feature("Product detail")
@allure.story("The cart survives a return to the catalogue")
def test_back_to_products_returns_to_the_catalogue_with_the_cart_intact(
    logged_in_inventory_page: InventoryPage,
) -> None:
    detail_page = logged_in_inventory_page.open_product_detail(BACKPACK)
    detail_page.add_to_cart()
    detail_page.back_to_products()

    logged_in_inventory_page.expect_loaded()
    expect(logged_in_inventory_page.header.cart_badge).to_have_text("1")
    expect(logged_in_inventory_page.products.button_for(BACKPACK)).to_have_text(
        "Remove"
    )


@pytest.mark.manual_case("TC-INV-011")
@allure.feature("Product detail")
@allure.story("A product can be removed from its detail page")
def test_product_can_be_removed_from_its_detail_page(
    logged_in_inventory_page: InventoryPage,
) -> None:
    logged_in_inventory_page.add_product_to_cart(BACKPACK)
    detail_page = logged_in_inventory_page.open_product_detail(BACKPACK)
    detail_page.remove_from_cart()

    expect(detail_page.header.cart_badge).to_have_count(0)
    expect(detail_page.add_to_cart_button).to_be_visible()
