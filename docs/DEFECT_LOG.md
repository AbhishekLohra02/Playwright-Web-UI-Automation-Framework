# Defect log

Application defects observed in SauceDemo while building and running this suite.
Each was reproduced directly against the live site.

Defects injected deliberately by the special accounts are recorded here rather
than asserted in the suite: they are fixtures of the demo application, and
encoding them as expected results would document bugs as requirements. See
`TEST_STRATEGY.md` for how those accounts are used instead.

---

## SD-001 — Item Total renders a raw floating-point value

**Severity:** Major  **Area:** Checkout  **Account:** all, including `standard_user`

The order overview prints the item total without rounding it to a currency
value, so JavaScript floating-point error reaches the screen.

**Reproduction.** Sign in as `standard_user`, add Backpack, Bike Light, Bolt
T-Shirt and Fleece Jacket, and continue to the order overview.

**Expected:** `Item total: $105.96`
**Actual:** `Item total: $105.96000000000001`

Observed with other combinations too, for example `$99.94999999999999`. Tax and
Total are rounded correctly, so only the subtotal is affected.

**Note for the suite.** Whether this reproduces depends entirely on which
products are selected; the default two-product selection sums cleanly and hides
it. A currency-format assertion, rather than an arithmetic one, would detect it
regardless of the combination.

---

## SD-002 — `error_user` passes checkout validation with an empty required field

**Severity:** Major  **Area:** Checkout  **Account:** `error_user`

Typing a last name into the customer-information form leaves the field empty,
yet Continue advances to the order overview instead of raising
`Error: Last Name is required`. The same input on `standard_user` is validated
correctly, and on `problem_user` the error is correctly raised.

**Expected:** Continue is blocked and the required-field error is shown.
**Actual:** The order overview is reached with no last name captured.

---

## SD-003 — `error_user` cannot complete an order

**Severity:** Critical  **Area:** Checkout  **Account:** `error_user`

On the order overview, Finish leaves the browser on
`/checkout-step-two.html`. No confirmation page is reached and no error is
displayed, so the transaction fails silently.

---

## SD-004 — `visual_user` displays prices unrelated to the catalogue

**Severity:** Major  **Area:** Product catalogue  **Account:** `visual_user`

Inventory prices are randomised on each session — `$48.93, $75.33, $98.16…`
then `$84.28, $71.07, $13.33…` — and match no catalogue price. Order totals are
still computed from the real prices, so the amount displayed to the customer
and the amount charged disagree.

---

## SD-005 — `problem_user` corrupts customer-information input

**Severity:** Major  **Area:** Checkout  **Account:** `problem_user`

Entering First Name "Abhishek" then Last Name "Sharma" results in First Name
"Sharma" and an empty Last Name: the last-name field writes into the first-name
field and clears itself.
