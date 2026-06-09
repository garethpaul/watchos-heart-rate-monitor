# WatchKit Authorization Main Thread

## Status: Completed

## Context

The WatchKit controller requested HealthKit read authorization and updated the
denied-permission label directly from the authorization callback. That callback
is not a UI-thread contract, so visible WatchKit feedback should be dispatched
to the main queue just like heart-rate sample updates already are.

## Objectives

- Preserve the existing HealthKit authorization request.
- Keep denied-authorization feedback visible.
- Dispatch denied-authorization UI updates onto the main queue.
- Keep the app source and UI-test mirror controller synchronized.
- Add static checker coverage for the UI-thread boundary.

## Work Completed

- Wrapped `displayNotAllowed()` in `dispatch_async(dispatch_get_main_queue())`
  for denied HealthKit authorization.
- Applied the same change to the duplicated WatchKit UI-test fixture.
- Extended `scripts/check_watchos_contracts.py` with mirrored authorization
  UI-thread coverage.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_watchos_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add manual device verification notes for HealthKit authorization prompts.
- Modernize HealthKit APIs in a dedicated compatibility pass.
