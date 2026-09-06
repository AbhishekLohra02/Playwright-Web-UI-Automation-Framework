"""The SauceDemo catalogue.

Prices mirror what the inventory page shows for `standard_user`, which is the
only account that renders the catalogue faithfully.
"""

from decimal import Decimal

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"
BOLT_T_SHIRT = "Sauce Labs Bolt T-Shirt"
FLEECE_JACKET = "Sauce Labs Fleece Jacket"
ONESIE = "Sauce Labs Onesie"
TEST_ALL_THE_THINGS_T_SHIRT = "Test.allTheThings() T-Shirt (Red)"

CATALOGUE = {
    BACKPACK: Decimal("29.99"),
    BIKE_LIGHT: Decimal("9.99"),
    BOLT_T_SHIRT: Decimal("15.99"),
    FLEECE_JACKET: Decimal("49.99"),
    ONESIE: Decimal("7.99"),
    TEST_ALL_THE_THINGS_T_SHIRT: Decimal("15.99"),
}

ALL_PRODUCTS = tuple(CATALOGUE)

# The representative selection used by cart and checkout scenarios.
CART_PRODUCTS = (
    BACKPACK,
    BIKE_LIGHT,
)

# Summing these four prices exposes SD-001: the order overview prints the item
# total as a raw floating-point value, `$105.96000000000001` instead of
# `$105.96`. Whether the defect appears depends entirely on the combination,
# which is why it hides behind a two-product selection.
FLOAT_ARTIFACT_PRODUCTS = (
    BACKPACK,
    BIKE_LIGHT,
    BOLT_T_SHIRT,
    FLEECE_JACKET,
)
