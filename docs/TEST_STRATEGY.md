# Test strategy

## Purpose

This document states what is tested, why those things and not others, and what
a green pipeline is actually claiming. It is the reference for anyone extending
the suite.

## Application under test

SauceDemo is a public demonstration storefront and a **third-party dependency**.
It can change or break without notice, which shapes two decisions: the suite
runs nightly rather than only on pull requests, and no test depends on data the
suite itself cannot re-establish.

## Risk-based scope

Automation follows business impact rather than screen count.

| Priority | Area | Reasoning |
|---|---|---|
| P1 | Authentication and session handling | Controls all access; a defect here is a security defect |
| P1 | Checkout completion and order totals | The revenue path and the money on screen |
| P2 | Cart contents | Protects the customer's selections between screens |
| P3 | Catalogue sorting | Visible but non-blocking; wrong order does not lose an order |

Highly visual, repetitive, or exploratory scenarios remain in the manual suite
and are tracked in the accompanying workbook.

## Test levels

Markers, not directories, define the levels, so one scenario can belong to
several without being duplicated.

| Marker | Purpose | Intended trigger |
|---|---|---|
| `smoke` | The main customer journey is usable at all | Every build; runs first and fails fast |
| `sanity` | Focused confirmation of changed or affected areas | Pull requests |
| `regression` | Complete automated functional coverage | Merges and the nightly run |

Area markers (`login`, `inventory`, `cart`, `checkout`, `accessibility`) allow a
failing area to be re-run in isolation during triage. `manual_case` records
which workbook cases a test covers and feeds the traceability matrix.

CI runs `smoke` as a separate step before the full suite, so a broken customer
journey is reported in seconds rather than after a full regression pass.

## Account matrix

SauceDemo publishes six accounts. They are the application's own oracle for
negative testing: each injects specific defects after sign-in. Behavior below
was verified directly against the live site.

| Account | Sign-in | Behavior once signed in |
|---|---|---|
| `standard_user` | Succeeds | Correct; the reference for all other accounts |
| `locked_out_user` | **Refused** | n/a |
| `problem_user` | Succeeds | Images all resolve to `sl-404.jpg`; sort dropdown is inert; 3 of 6 Add-to-cart buttons dead; last-name field corrupts typed input |
| `performance_glitch_user` | Succeeds, **~5s delay** | Otherwise correct |
| `error_user` | Succeeds | Sort broken; 3 Add-to-cart fail with a JS error; checkout continues past an empty required field; Finish never completes the order |
| `visual_user` | Succeeds | Prices randomised per session and unrelated to the real catalogue; header cart icon displaced ~185px |

**How the suite uses them.** Authentication is the boundary these accounts are
tested at: `test_login_accepted_users_can_sign_in.py` proves all five
sign-in-enabled accounts cross it and reach a catalogue of six products, and
`test_login_performance_budget.py` proves the harness can actually measure the
delay `performance_glitch_user` injects. The post-login defects are documented
in `DEFECT_LOG.md` rather than asserted, because they are deliberate fixtures of
the demo application, not regressions of it.

## Negative and edge coverage at sign-in

Beyond absent credentials, the suite asserts that authentication is exact and
does not leak behavior:

- Wrong case in either field is rejected.
- Leading or trailing whitespace is rejected rather than trimmed.
- A password wrong by one character is rejected.
- SQL- and script-injection payloads and 300-character input return the same
  generic failure message as any other bad credential, proving the payload was
  neither interpreted nor acknowledged as special.
- The error banner can be dismissed and the sign-in retried without a reload.
- The password field is masked.
- The catalogue is unreachable by direct URL, and the browser Back button does
  not restore a signed-out session.

## Framework architecture

The Page Object Model is the architecture; the reporting layer sits on top of
it and does not shape it.

- **Pages** own locators and expose actions. They never assert business rules;
  tests do.
- **Components** are widgets shared by several screens — the header and the
  repeated product-row collection — composed into pages rather than inherited.
  This keeps the page hierarchy describing pages instead of accumulating
  widgets, and keeps shared locators in one file.
- **Navigation returns the next page object** and asserts arrival, so a test
  reads as a journey. Actions used by negative tests deliberately return
  nothing, because promising a destination a negative test does not reach would
  be a lie encoded in the API.
- **Reporting metadata is derived, not repeated.** Allure's epic, severity and
  traceability tags come from the pytest markers a test already carries, so
  area, level and manual-case coverage are declared once and cannot drift
  between selection, reporting and the traceability matrix.
- **Types are checked.** mypy runs over pages, tests, fixtures and scripts with
  `disallow_untyped_defs`, so the fluent navigation contract - which page each
  action returns - is verified rather than assumed.
- **Timeouts are explicit.** Assertion, action and navigation budgets are set in
  `conftest.py` rather than inherited from Playwright's defaults, because an
  implicit five-second assertion budget is a decision nobody made and the usual
  cause of a "flaky" suite on a loaded runner.

## Environments

The base URL is supplied by `pytest-base-url` through the `base_url` key in
`pytest.ini`, overridable per run with `--base-url` or `PYTEST_BASE_URL`. No
URL is hard-coded in a page object or a test.

## Execution

- **Parallel by default in CI** via `pytest-xdist` (`--numprocesses auto`).
  Every test creates its own browser context and signs in independently, so
  there is no shared state to serialise.
- **No automatic retries.** A flaky test is treated as a defect in the test, not
  absorbed by a rerun. Traces and screenshots are retained on failure precisely
  so a flake can be diagnosed rather than re-run.
- **Nightly regression** at 02:00 UTC catches third-party breakage between pull
  requests, and widens to Firefox and WebKit. Pull requests stay on Chromium so
  feedback stays fast.
- **Weekly flake detection** repeats the smoke and sanity tests five times and
  fails if any run disagrees with another. A no-retries policy is only
  believable if something checks it.
- **Reproducible environments.** A `Dockerfile` pins the browser stack and
  system libraries, so a local run and a CI run execute the same thing.

## Reporting

| Output | Purpose |
|---|---|
| Allure report | Primary human-facing report: epic/feature/story, severity, step detail, failure screenshots |
| GitHub job summary | Pass/fail table visible without downloading anything |
| `junit.xml` | Machine-readable results for CI integrations |
| `report.html` | Portable self-contained report |
| Playwright traces | Failure-only, for step-by-step replay |

## Accessibility

The main journey is scanned with axe-core. **Critical and serious violations
fail the build**; moderate and minor findings are attached to the Allure report
and tracked in the defect log, because blocking on structural landmark warnings
would stall delivery over issues that stop nobody completing a purchase.

Login, cart and checkout are clean at that gate. The inventory page is not:
SD-007, an unlabelled sort control, is pinned as a strict xfail.

## Coverage

Requirement coverage is traced against the manual workbook and published as
`TRACEABILITY.md`, generated by `scripts/traceability.py` from the workbook and
the `manual_case` markers. CI regenerates it and fails if the committed file is
stale, so the matrix cannot drift from either side. 47 of 58 manual cases are
automated.

**Line coverage is deliberately not reported.**
`coverage.py` cannot trace the sync Playwright API accurately: that API runs
user code inside a greenlet, and the tracer does not follow greenlet switches,
so every statement after the first Playwright call in a method is wrongly
reported as unexecuted. A measured 94% under those conditions is noise, and
publishing it would be misleading.

## Entry and exit criteria

**Entry.** Lint and formatting pass; the application is reachable.

**Exit.** All `smoke` tests pass, no unexplained failures in `regression`, and
any new failure is either fixed or recorded in `DEFECT_LOG.md` with an owner.

## Known limitations

- Firefox and WebKit run nightly rather than on every pull request.
- Product names and `data-test` attributes are treated as stable contracts.
- Test data is public demo data and contains no secrets.
