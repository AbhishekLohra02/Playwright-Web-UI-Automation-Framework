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
- Page Object Model

## Automated scope

| Module | Automated coverage | Executions |
|---|---|---:|
| Login | Successful login, locked-out user, invalid credentials, required fields | 8 |
| Cart | Retain multiple products, remove a selected product | 2 |
| Checkout | Successful order, dynamic Item Total, required customer information | 5 |
| **Total** | | **15** |

The automated suite uses representative products and data-driven scenarios rather
than repeating identical behavior for every product or user.

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
|   |-- login_page.py
|   |-- inventory_page.py
|   |-- cart_page.py
|   |-- checkout_information_page.py
|   |-- checkout_overview_page.py
|   `-- checkout_complete_page.py
|-- test_data/              # Reusable users, products, and customer data
|   |-- users.py
|   |-- products.py
|   `-- customers.py
|-- tests/                  # Independent Pytest scenarios
|-- conftest.py             # Shared fixtures and test setup
|-- pytest.ini              # Pytest discovery and output configuration
|-- requirements.txt        # Pinned Python dependencies
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

`pytest.ini` configures test discovery, verbose output, and short tracebacks.

## Continuous integration and reporting

The GitHub Actions workflow in `.github/workflows/playwright-tests.yml` runs the
complete Chromium suite automatically on:

- Pushes to `main`
- Pull requests targeting `main`
- Manual workflow execution

Each CI run creates one downloadable `playwright-test-artifacts` archive containing:

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

Shared setup is defined in `conftest.py`:

- `base_url` provides the SauceDemo URL for the test session.
- `configure_test_id_attribute` configures Playwright's test-ID engine to use
  SauceDemo's `data-test` attribute.
- `login_page` creates a fresh Login page for each test.
- `logged_in_inventory_page` performs the standard-user login and returns an
  Inventory page for authenticated Cart and Checkout scenarios.

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
- Checkout Item Total validation compares product prices before tax; tax and the
  final post-tax total are outside that test's scope.
- Test data contains public demo values and no production secrets.
- GitHub Actions executes the Chromium regression suite and publishes JUnit,
  HTML, trace, and screenshot artifacts where applicable.
- Manual test documentation must be included in the repository before final
  assignment submission.

## Future improvements

- Smoke and regression markers
- Parallel and cross-browser execution
- Environment-based URL configuration
- Historical test-result dashboard and trend analysis
