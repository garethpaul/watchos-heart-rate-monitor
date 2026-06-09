# WatchKit Inactive Heart-Rate Callbacks

Status: Completed

## Context

The WatchKit controller retains and stops the active heart-rate query when a
workout ends or fails. HealthKit callbacks can still arrive around the same
time as shutdown, and the streaming query closures updated the anchor and UI
without first checking whether the workout was still active.

## Plan

- Guard the initial anchored-query callback before anchor or UI updates.
- Guard the update-handler callback before anchor or UI updates.
- Mirror the same guard in the duplicated UI-test WatchKit controller.
- Extend `scripts/check_watchos_contracts.py` so both controller copies keep
  inactive callback guards before anchor updates.

## Verification

- `python3 scripts/check_watchos_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

On this non-macOS host, `make verify` runs the static checks and skips Xcode
because `xcodebuild` is unavailable.
