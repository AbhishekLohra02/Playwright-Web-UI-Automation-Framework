"""SauceDemo accounts.

The site publishes every accepted username on the login page. Each account
behaves differently once signed in, which makes them the site's own oracle for
negative and edge-case login testing.
"""

PASSWORD = "secret_sauce"

# Signs in and behaves normally.
STANDARD_USERNAME = "standard_user"

# Rejected at the login step.
LOCKED_OUT_USERNAME = "locked_out_user"

# Sign in successfully but serve deliberately broken behavior afterwards.
PROBLEM_USERNAME = "problem_user"
PERFORMANCE_GLITCH_USERNAME = "performance_glitch_user"
ERROR_USERNAME = "error_user"
VISUAL_USERNAME = "visual_user"

# Every account the login page advertises as accepted.
ACCEPTED_USERNAMES = (
    STANDARD_USERNAME,
    LOCKED_OUT_USERNAME,
    PROBLEM_USERNAME,
    PERFORMANCE_GLITCH_USERNAME,
    ERROR_USERNAME,
    VISUAL_USERNAME,
)

# Accepted accounts that are expected to reach the inventory.
SIGN_IN_ENABLED_USERNAMES = (
    STANDARD_USERNAME,
    PROBLEM_USERNAME,
    PERFORMANCE_GLITCH_USERNAME,
    ERROR_USERNAME,
    VISUAL_USERNAME,
)

# Credentials that must never be accepted.
UNKNOWN_USERNAME = "unknown_user"
INVALID_PASSWORD = "invalid_password"
