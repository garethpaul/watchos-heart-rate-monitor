# WatchKit Authorization Start Button State

## Status: Completed

## Context

The WatchKit controller displayed `not available` or `not allowed` when
HealthKit could not be used, but the Start button remained enabled. That made
the UI suggest a workout could start even while HealthKit authorization was
unavailable, denied, or still pending.

## Objectives

- Disable Start when HealthKit data is unavailable.
- Disable Start while HealthKit authorization is pending.
- Disable Start when HealthKit authorization is denied.
- Re-enable Start on the main queue after successful authorization.
- Keep the app controller and UI-test mirror synchronized.

## Work Completed

- Disabled the Start button in the HealthKit-unavailable branch.
- Disabled the Start button before requesting HealthKit authorization.
- Re-enabled the Start button after successful authorization on the main queue.
- Updated `displayNotAllowed()` to disable Start for denied authorization.
- Mirrored the controller changes in the UI-test fixture.
- Added static contract coverage for both controller copies.
- Updated README, SECURITY, VISION, and CHANGES.

## Verification

- `python3 scripts/check_watchos_contracts.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
