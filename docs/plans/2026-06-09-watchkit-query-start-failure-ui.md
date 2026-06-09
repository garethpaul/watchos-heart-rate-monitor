# WatchKit Query Start Failure UI

## Status: Completed

## Context

When a workout session reached the running state, the controller attempted to
create and execute a heart-rate streaming query. If query creation failed, the
sample only changed the label to `cannot start`; the workout active flag,
button title, and retained workout session could still look active.

## Objectives

- Preserve the existing workout start and heart-rate streaming flow.
- Reset workout active state when query creation fails.
- Restore the Start button title on query startup failure.
- End and clear the retained workout session when no heart-rate query can run.
- Keep the app source and UI-test mirror controllers synchronized.

## Work Completed

- Updated both WatchKit `InterfaceController.swift` copies to reset
  `workoutActive` on query creation failure.
- Restored the Start button title before showing `cannot start`.
- Ended any retained workout session and cleared controller session state.
- Extended `scripts/check_watchos_contracts.py` with mirrored query-start
  failure checks.
- Updated README, VISION, and CHANGES.

## Verification

- Negative check: `python3 scripts/check_watchos_contracts.py` failed before
  the query-start failure reset was added.
- `python3 scripts/check_watchos_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add manual device verification notes for HealthKit query startup failures.
- Modernize HealthKit APIs in a dedicated compatibility pass.
