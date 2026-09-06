import allure
import pytest
from playwright.sync_api import expect

from pages.checkout_information_page import CheckoutInformationPage
from test_data.customers import FIRST_NAME, LAST_NAME, POSTAL_CODE
from test_data.messages import (
    FIRST_NAME_REQUIRED,
    LAST_NAME_REQUIRED,
    POSTAL_CODE_REQUIRED,
)

pytestmark = [pytest.mark.checkout, pytest.mark.regression]


@allure.feature("Customer information")
@allure.story("Required fields are enforced")
@pytest.mark.sanity
@pytest.mark.parametrize(
    ("first_name", "last_name", "postal_code", "expected_error"),
    [
        pytest.param(
            "",
            LAST_NAME,
            POSTAL_CODE,
            FIRST_NAME_REQUIRED,
            id="missing_first_name",
        ),
        pytest.param(
            FIRST_NAME,
            "",
            POSTAL_CODE,
            LAST_NAME_REQUIRED,
            id="missing_last_name",
        ),
        pytest.param(
            FIRST_NAME,
            LAST_NAME,
            "",
            POSTAL_CODE_REQUIRED,
            id="missing_postal_code",
        ),
    ],
)
def test_checkout_validates_required_customer_information(
    checkout_information_page: CheckoutInformationPage,
    first_name: str,
    last_name: str,
    postal_code: str,
    expected_error: str,
) -> None:
    checkout_information_page.enter_details(first_name, last_name, postal_code)
    checkout_information_page.click_continue()

    checkout_information_page.expect_loaded()
    expect(checkout_information_page.error_message).to_be_visible()
    expect(checkout_information_page.error_message).to_have_text(expected_error)
