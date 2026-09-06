"""Render a JUnit XML result file as a GitHub Actions job summary table.

CI results are useless if reading them means downloading a zip. This turns the
run into a table on the workflow summary page, and lists any failures inline.
"""

import sys
import xml.etree.ElementTree as ElementTree
from pathlib import Path


def main(junit_path: str) -> int:
    path = Path(junit_path)
    if not path.exists():
        print(f"No JUnit results found at `{junit_path}`.")
        return 0

    root = ElementTree.parse(path).getroot()
    suites = root.iter("testsuite") if root.tag == "testsuites" else [root]

    totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0, "time": 0.0}
    failures: list[tuple[str, str]] = []

    for suite in suites:
        for key in ("tests", "failures", "errors", "skipped"):
            totals[key] += int(suite.get(key, 0))
        totals["time"] += float(suite.get("time", 0.0))

        for case in suite.iter("testcase"):
            for problem in list(case.iter("failure")) + list(case.iter("error")):
                name = f"{case.get('classname', '')}::{case.get('name', '')}"
                failures.append((name, (problem.get("message") or "").strip()))

    passed = totals["tests"] - totals["failures"] - totals["errors"] - totals["skipped"]

    print("## Playwright test results\n")
    print("| Total | Passed | Failed | Errors | Skipped | Duration |")
    print("|------:|-------:|-------:|-------:|--------:|---------:|")
    print(
        f"| {totals['tests']} | {passed} | {totals['failures']} | "
        f"{totals['errors']} | {totals['skipped']} | {totals['time']:.1f}s |"
    )

    if failures:
        print("\n### Failures\n")
        for name, message in failures:
            first_line = message.splitlines()[0] if message else "no message"
            print(f"- `{name}`")
            print(f"  - {first_line}")
    else:
        print("\nAll tests passed.")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "test-results/junit.xml"))
