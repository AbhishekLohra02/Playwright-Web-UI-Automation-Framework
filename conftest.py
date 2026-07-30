import pytest


@pytest.fixture(scope="session")
def base_url():
    return "https://www.saucedemo.com/"


@pytest.fixture(scope="session", autouse=True)
def configure_test_id_attribute(playwright):
    playwright.selectors.set_test_id_attribute("data-test")
