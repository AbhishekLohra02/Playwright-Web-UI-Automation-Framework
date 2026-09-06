import time

import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.users import (
    PASSWORD,
    PERFORMANCE_GLITCH_USERNAME,
    STANDARD_USERNAME,
)

pytestmark = [pytest.mark.login, pytest.mark.regression]

# The glitch account delays the sign-in response by roughly five seconds.
# The margin is deliberately loose so the check measures the injected delay
# rather than the speed of the machine running it.
MINIMUM_INJECTED_DELAY_SECONDS = 2.0
STANDARD_LOGIN_BUDGET_SECONDS = 10.0


def _measure_login(login_page: LoginPage, username: str) -> float:
    started = time.perf_counter()
    login_page.login(username, PASSWORD)
    InventoryPage(login_page.page).expect_loaded()
    return time.perf_counter() - started


@allure.epic("Authentication")
@allure.feature("Sign in")
@allure.story("Sign-in stays within its performance budget")
@allure.severity(allure.severity_level.NORMAL)
def test_standard_user_signs_in_within_budget(login_page: LoginPage) -> None:
    elapsed = _measure_login(login_page, STANDARD_USERNAME)

    allure.attach(
        f"{elapsed:.2f}s",
        name="standard_user sign-in",
        attachment_type=allure.attachment_type.TEXT,
    )

    assert elapsed < STANDARD_LOGIN_BUDGET_SECONDS, (
        f"standard_user sign-in took {elapsed:.2f}s, "
        f"budget is {STANDARD_LOGIN_BUDGET_SECONDS}s"
    )


@allure.epic("Authentication")
@allure.feature("Sign in")
@allure.story("The performance-glitch account is measurably degraded")
@allure.severity(allure.severity_level.NORMAL)
def test_performance_glitch_user_sign_in_is_measurably_slower(
    page, login_page: LoginPage
) -> None:
    """Prove the harness can actually detect a slow sign-in.

    Comparing the two accounts in one browser session makes this a relative
    measurement, so it stays meaningful on a loaded CI runner where an absolute
    threshold would be flaky.
    """
    standard_seconds = _measure_login(login_page, STANDARD_USERNAME)

    InventoryPage(page).logout()
    glitch_seconds = _measure_login(login_page, PERFORMANCE_GLITCH_USERNAME)

    allure.attach(
        f"standard_user: {standard_seconds:.2f}s\n"
        f"performance_glitch_user: {glitch_seconds:.2f}s",
        name="Sign-in timings",
        attachment_type=allure.attachment_type.TEXT,
    )

    assert glitch_seconds > standard_seconds + MINIMUM_INJECTED_DELAY_SECONDS, (
        f"performance_glitch_user signed in in {glitch_seconds:.2f}s versus "
        f"{standard_seconds:.2f}s for standard_user; the injected delay was "
        f"not detected"
    )
