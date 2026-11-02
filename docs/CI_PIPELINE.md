# CI Pipeline Documentation

## Overview

The GitHub Actions workflow in `.github/workflows/ci.yml` runs for pushes to
`main` and `develop`, and for pull requests targeting either branch. It checks
Python compilation and style, runs the test suite, records test and coverage
reports, and checks the Iris model against its minimum accuracy threshold.

The workflow uses Python 3.11 and installs the project dependencies from
`requirements.txt`.

## Jobs and dependency order

The jobs run in this order:

```text
build-and-lint
      |
      v
test-suite
      |
      v
model-quality-gate
```

### `build-and-lint`

This job checks out the repository, installs dependencies and the CI testing
tools, compiles Python files in `src` and `tests`, then runs Flake8 on `src`
with a maximum line length of 100 characters. It must pass before
`test-suite` starts.

### `test-suite`

This job depends on `build-and-lint`. It collects the Iris data and runs the
preprocessing and feature-engineering pipeline scripts before running all
tests under `tests/`. Pytest produces JUnit XML (`test-results.xml`) and
coverage XML (`coverage.xml`); both are uploaded as the
`test-and-coverage-reports` workflow artifact when available.

The pipeline scripts use their default input and output paths. In particular,
they do not accept the command-line arguments shown in some earlier procedure
notes.

### `model-quality-gate`

This job depends on `test-suite`. It prepares the Iris feature data and runs
`tests/test_model_quality.py`, which asserts that model accuracy meets
`MIN_ACCEPTABLE_ACCURACY` (normally `0.90`).

Because `test-suite` currently runs the complete test collection, including
`test_model_quality.py`, this dedicated job repeats that quality test after a
successful suite. If the quality test fails in `test-suite`, the dependent
`model-quality-gate` job is skipped by GitHub Actions due to `needs:`.

## Branch protection

Configure a GitHub branch ruleset targeting `main` (for example, **Protect
main - CI checks**) with enforcement active. Require pull requests and require
the following checks to pass before merging:

- `build-and-lint`
- `test-suite`
- `model-quality-gate`

Enable the requirement for branches to be up to date before merging if that
option is available. The ruleset is configured in GitHub repository settings;
the workflow file alone cannot enforce branch protection.

## Pull request verification

A pull request targeting `main` or `develop` should trigger the workflow. The
three job checks appear on the pull request, and the test and coverage reports
can be downloaded from the completed workflow run's artifacts.

## Model-quality regression demonstration

The regression demonstration is performed on a temporary feature branch, not
on `main`:

1. Change `MIN_ACCEPTABLE_ACCURACY` in `tests/test_model_quality.py` from
   `0.90` to `0.999`.
2. Push the branch and open a pull request targeting `main`.
3. Confirm that the model-quality assertion fails and that the required
   checks prevent merging.
4. Close the demonstration pull request without merging, delete the temporary
   branch, and verify that the normal `0.90` threshold remains on `main`.

In the recorded demonstration, the model accuracy was approximately `0.9667`
(`96.67%`), below the temporary `0.999` (`99.9%`) threshold. The complete test
suite reported 15 passing tests and one failing test. Since the suite includes
the model-quality test, the regression was detected in `test-suite`; the
separate `model-quality-gate` was skipped because it depends on that suite.
This demonstrates test-based regression detection, but the separate
model-quality job does not independently execute for that failing run.

## Viva-voce questions

### Why use `needs:` between jobs?

`needs:` establishes job dependencies, so each downstream job waits for its
prerequisite to succeed. This gives failures a clear order and avoids running
later checks when an earlier required check has failed. Removing these
dependencies would allow the jobs to run in parallel, consuming runner time
even when an upstream quality check fails.

### Why require CI checks instead of relying on local pytest runs?

Local test runs are not an enforceable merge requirement and may use different
environments. Required status checks make the configured CI results a
consistent, repository-enforced condition for merging into the protected
branch.

### Why deliberately introduce a failing threshold?

A passing run shows that the current code passed, but does not by itself prove
that a quality check detects a known-bad condition. Raising the threshold on a
temporary branch tests that the model-quality assertion fails as expected and
that the pull request reports the failure. The branch must not be merged.
