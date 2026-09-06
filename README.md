# SauceDemo Test Automation Framework

[![Playwright Tests](https://github.com/AbhishekLohra02/SauceDemo_Test_Automation_Framework/actions/workflows/playwright-tests.yml/badge.svg)](https://github.com/AbhishekLohra02/SauceDemo_Test_Automation_Framework/actions/workflows/playwright-tests.yml)

Python UI automation framework for [SauceDemo](https://www.saucedemo.com/),
created as part of a QA Automation Engineer assignment.

The project uses Pytest, Playwright for Python, and the Page Object Model (POM).
Automation focuses on stable, business-critical Login, Cart, and Checkout flows.

## Technology stack

- Python 3.11
- Pytest 9.1.1
- Playwright 1.61.0
- pytest-playwright 0.8.0
- pytest-html 4.2.0
- pytest-xdist 3.8.0 for parallel execution
- allure-pytest 2.16.0 for reporting
- Ruff 0.14.5 for linting and formatting
- mypy 1.18.2 for static type checking
- axe-core via axe-playwright-python for accessibility checks
- Page Object Model

## Automated scope

| Module | Automated coverage | Executions |
|---|---|---:|
| Login | Every accepted account signs in, locked-out account refused, invalid credentials, case and whitespace exactness, injection and oversized input, required fields, error dismissal and retry, keyboard submit, masked password, sign-in performance budget | 31 |
| Session | Unauthenticated URL access, logout, browser-Back after logout | (included above) |
| Inventory | Sorting by price and name, product detail page, remove from the listing, Reset App State | 10 |
| Cart | Retain multiple products, remove a selected product, continue shopping | 3 |
| Checkout | Successful order, confirmation and emptied cart, Item Total, currency formatting, tax and payable total, required customer information, cancelling an order | 12 |
| Accessibility | axe-core scans of login, catalogue, cart and checkout | 4 |
| **Total** | | **60** |

Three of those are `xfail(strict=True)`, pinning application defects SD-001,
SD-006 and SD-007 from the [defect log](./docs/DEFECT_LOG.md). Strict marking
means that if SauceDemo ever fixes them, the suite fails and tells us to remove
the marker.

The automated suite uses representative products and data-driven scenarios rather
than repeating identical behavior for every product or user.

## Test strategy and defects

- [Test strategy](./docs/TEST_STRATEGY.md) — risk-based scope, test levels, the
  SauceDemo account matrix, execution and reporting policy, and why line
  coverage is deliberately not published.
- [Defect log](./docs/DEFECT_LOG.md) — application defects found against the
  live site while building this suite, including a floating-point leak in the
  checkout Item Total that affects `standard_user`.
- [Traceability matrix](./docs/TRACEABILITY.md) — generated, never hand-edited,
  mapping every manual workbook case to the automated tests that cover it.
  CI fails if the committed file is stale.

## Manual test documentation

The focused, risk-based manual test suite is available here:

[Download the manual test suite](./SauceDemo_Manual_Test_Cases_Focused_With_Automation_Mapping.xlsx)

The workbook includes test objectives, priorities, preconditions, test data,
test steps, expected results, exploratory charters, automation status, and
traceability between manual cases and the implemented automated tests.

## Project structure

```text
SauceDemo_Test_Automation/
|-- pages/                  # Page Objects, locators, and page actions
|   |-- components/         # Reusable widgets composed into pages
|   |   |-- header.py       # Banner, cart badge, and menu
|   |   `-- product_collection.py  # Repeated product rows
|   |-- base_page.py        # BasePage and AuthenticatedPage shared behavior
|   |-- prices.py           # Displayed-price parsing helper
|   |-- login_page.py
|   |-- product_detail_page.py
|   |-- inventory_page.py
|   |-- cart_page.py
|   |-- checkout_information_page.py
|   |-- checkout_overview_page.py
|   `-- checkout_complete_page.py
|-- test_data/              # Reusable users, products, customers, messages
|   |-- users.py
|   |-- products.py
|   |-- customers.py
|   `-- messages.py
|-- tests/                  # Independent Pytest scenarios
|-- docs/                   # Test strategy and defect log
|   |-- TEST_STRATEGY.md
|   `-- DEFECT_LOG.md
|-- scripts/                # CI helpers
|   |-- junit_summary.py    # Renders JUnit results as a GitHub job summary
|   `-- traceability.py     # Regenerates docs/TRACEABILITY.md
|-- Dockerfile              # Reproducible browser and dependency stack
|-- pyproject.toml          # Pytest, Ruff, and mypy configuration
|-- conftest.py             # Shared fixtures and test setup
|-- .pre-commit-config.yaml # Local lint hooks
|-- requirements.txt        # Pinned runtime dependencies
|-- requirements-dev.txt    # Pinned lint and tooling dependencies
`-- README.md
```

## Prerequisites

- Python 3.11 or a compatible Python 3 version
- Git
- Internet access to SauceDemo

## Setup

Clone the repository:

```bash
git clone https://github.com/AbhishekLohra02/SauceDemo_Test_Automation_Framework.git
cd SauceDemo_Test_Automation_Framework
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it in Git Bash:

```bash
source .venv/Scripts/activate
```

Or activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the pinned dependencies:

```bash
python -m pip install -r requirements.txt
```

Install the lint and formatting tooling as well when contributing:

```bash
python -m pip install -r requirements-dev.txt
pre-commit install
```

Install the Chromium browser used by Playwright:

```bash
python -m playwright install chromium
```

## Test execution

Run the complete suite headlessly:

```bash
python -m pytest
```

Run the complete suite with a visible browser:

```bash
python -m pytest --headed
```

Run one module or scenario file:

```bash
python -m pytest tests/test_checkout_completes_order_successfully.py --headed
```

Run with an explicit browser selection:

```bash
python -m pytest --browser chromium
```

Generate a self-contained HTML report locally:

```bash
python -m pytest --html=reports/report.html --self-contained-html
```

Open the generated file in a browser:

```text
reports/report.html
```

Run a single test category using markers:

```bash
python -m pytest -m smoke
python -m pytest -m "checkout and not smoke"
python -m pytest -m login
```

Run the suite in parallel:

```bash
python -m pytest --numprocesses auto
```

Run against a different environment without editing code:

```bash
python -m pytest --base-url https://www.saucedemo.com/
```

`pytest.ini` configures test discovery, the default base URL, verbose output,
short tracebacks, strict markers, and failure-only traces and screenshots.
Because tracing and screenshots are configured there rather than in CI, a local
failure produces the same artifacts a CI failure does, under `test-results/`.

## Allure reporting

Every run writes Allure results to `allure-results/`. Allure Report is open
source and free; only the separate Allure TestOps product is commercial.

Install the CLI once (it needs a JRE), then generate and open the report:

```bash
allure serve allure-results
```

Page-object actions are recorded as steps, and a failing test attaches the URL
and a full-page screenshot taken at the moment of failure.

Report metadata is derived rather than repeated. The `epic` comes from the area
marker a test already carries and the `severity` from its level marker, both in
`pytest_collection_modifyitems`, so `pytest.mark.checkout` is the single source
of truth for both test selection and reporting. Only `feature` and `story`,
which carry information no marker holds, are written on the test itself.

## Code quality

Ruff and mypy are configured in `pyproject.toml`, alongside the pytest
settings, so all tool configuration lives in one file:

```bash
python -m ruff check .
python -m ruff format .
python -m mypy
```

mypy runs with `disallow_untyped_defs` across pages, tests, fixtures and
scripts, which is what verifies the fluent navigation contract — that each
action really does return the page object it claims.

The same checks run as a `pre-commit` hook locally and as a required
`static-analysis` job in CI, which the UI test job depends on.

## Running in Docker

Development happens on Windows and CI runs on Ubuntu, which is where most
"passes locally, fails in CI" reports come from. The image pins the browser
stack so both execute the same thing:

```bash
docker build -t saucedemo-tests .
docker run --rm saucedemo-tests
docker run --rm saucedemo-tests -m smoke --browser firefox
```

## Continuous integration and reporting

The GitHub Actions workflow in `.github/workflows/playwright-tests.yml` runs
Ruff and then the complete Chromium suite automatically on:

- Pushes to `main`
- Pull requests targeting `main`
- A nightly schedule at 02:00 UTC, because SauceDemo is a third-party
  dependency that can break between pull requests
- Manual workflow execution

The pipeline runs Ruff first, then the UI suite in parallel with
`--numprocesses auto`, with the Playwright browser binaries cached between runs.
A pass/fail table is written to the workflow summary page, so results are
readable without downloading anything.

Each CI run creates one downloadable `playwright-test-artifacts` archive containing:

- `allure-report/`: the generated Allure report
- `allure-results/`: raw Allure results, for merging trend history
- `reports/report.html`: portable, self-contained HTML test report
- `test-results/junit.xml`: machine-readable test results
- Playwright traces and screenshots retained when tests fail

The artifact is uploaded for successful and failed test runs and retained for 14
days. It can be downloaded from the workflow-run summary under **Artifacts**.

## Architecture

### Page Object Model

Each application screen has a dedicated Page Object. Page Objects own their
locators and expose meaningful actions, while tests own the scenario flow and
assertions.

`BasePage` holds the Playwright `Page`, the path each screen owns as `url_path`,
and an `expect_loaded()` navigation guarantee, so tests assert arrival on a page
through the page object instead of concatenating URL strings.

**Components over inheritance.** Widgets that appear on several screens are
composed in, not inherited. `AuthenticatedPage` owns a `HeaderComponent`
(`page.header.cart_badge`, `page.header.logout()`), because a cart page is not a
kind of header — it has one. `ProductCollection` wraps the repeated product-row
markup shared by the inventory grid, the cart and the order overview, so
filtering a row by name and parsing its price exist once rather than in three
page objects.

**Navigation returns the next page.** Actions that move between screens return
the page object for where they land and assert arrival on the way:

```python
information_page = inventory_page.header.open_cart().start_checkout()
overview_page = information_page.continue_to_overview()
complete_page = overview_page.finish_checkout()
```

Tests therefore read as journeys instead of constructor calls, and the page
objects — not the tests — hold the knowledge of what follows what. Where a
negative test expects to stay put, a raw variant makes no such promise:
`login()` and `click_continue()` submit without asserting a destination, while
`login_as()` and `continue_to_overview()` are the happy-path counterparts.

For example:

```text
LoginPage.login()
        |
        v
InventoryPage.add_product_to_cart()
        |
        v
CartPage.start_checkout()
        |
        v
CheckoutInformationPage.enter_details()
        |
        v
CheckoutOverviewPage.finish_checkout()
        |
        v
CheckoutCompletePage confirmation
```

All Page Objects receive the same Playwright `Page` instance during navigation.
The browser tab changes URL and content, and the next Page Object wraps that same
tab to expose the new screen's behavior.

### Fixture design

Shared setup is defined in `conftest.py` as a chain, so each test enters at the
exact state its scenario needs and no test repeats another test's setup:

- `configure_test_id_attribute` configures Playwright's test-ID engine to use
  SauceDemo's `data-test` attribute.
- `login_page` creates a fresh Login page for each test.
- `logged_in_inventory_page` performs the standard-user login and returns an
  Inventory page for authenticated Cart and Checkout scenarios.
- `cart_with_products` adds the selected products and opens the cart.
- `checkout_information_page` starts checkout from that cart.
- `checkout_overview_page` submits valid customer information and returns the
  order overview.

The base URL is not a project fixture. It is supplied by `pytest-base-url`
through the `base_url` key in `pytest.ini`, which means it can be overridden per
run with `--base-url` or the `PYTEST_BASE_URL` environment variable, and is
injected into the Playwright browser context so page objects navigate with
relative paths.

Function-scoped browser state keeps tests isolated and prevents cart or login
state from leaking between executions.

### Locator strategy

Locators are selected according to user meaning and stability:

1. Role and accessible name for semantic controls such as Login, Checkout,
   Continue, Finish, and the order-confirmation heading.
2. Placeholder locators for Checkout form fields that do not expose properly
   associated labels.
3. `data-test` attributes for stable application structures such as inventory
   rows, cart rows, badges, totals, and error messages.
4. Exact visible product names to filter a repeated product-row collection.

Position-based selectors, brittle XPath expressions, and generated CSS classes
are avoided. Product selection does not depend on catalogue order.

### Assertion strategy

- Playwright `expect()` assertions validate browser state and automatically retry
  while the UI is updating.
- Exact error text validates the correct business rule, not merely the presence
  of an error container.
- Row counts are calculated from the selected product collection rather than
  hard-coded.
- Python `assert` compares extracted `Decimal` values for the Checkout Item Total
  calculation because those values are Python data rather than Playwright
  locators.
- Hard waits such as `time.sleep()` are not used.

### Test data design

Reusable data is separated by domain:

- `users.py` contains authentication users and passwords.
- `products.py` contains product names and selected product collections.
- `customers.py` contains valid Checkout customer information.

Parameterized negative tests reuse the same workflow with different input and
expected-result combinations.

## Risk-based test selection

Automation prioritizes workflows with the greatest business impact:

- Authentication controls application access.
- Cart behavior protects the customer's selected products.
- Checkout completion protects the primary transaction journey.
- Required-field and calculation checks cover high-value negative and financial
  risks.

Lower-priority, highly visual, repetitive, or less critical scenarios remain in
the manual suite due to the assignment time constraint.

## Assumptions and limitations

- SauceDemo is available and its public test credentials remain valid.
- Chromium is the primary verified browser.
- Product names and `data-test` attributes are treated as stable contracts.
- Checkout validation covers the Item Total, the 8% tax, and the payable total.
- Test data contains public demo values and no production secrets.
- GitHub Actions executes the Chromium regression suite and publishes JUnit,
  HTML, trace, and screenshot artifacts where applicable.
- Manual test documentation is included in the repository as an Excel workbook.

## Future improvements

- Visual regression baselines for the catalogue and checkout
- A quarantine marker and dashboard for tests under investigation
- Contract checks against the SauceDemo endpoints to isolate UI from data
  failures
