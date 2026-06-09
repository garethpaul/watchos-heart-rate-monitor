# WatchKit UITest Query Mirror Plan

Date: 2026-06-08

Status: Completed

## Goal

Keep the duplicated WatchKit controller under `HeartyMonitorUITests/` aligned
with the safer HealthKit query lifecycle used by the main extension target.

## Scope

- Retain the active heart-rate query in the duplicated WatchKit controller.
- Stop and clear the same retained query when a workout ends.
- Guard `newAnchor` in the duplicated update handler instead of force-unwrapping.
- Extend the dependency-free WatchKit checker to validate both controller copies.

## TDD Notes

- Red: `python3 scripts/check_watchos_contracts.py` failed because this plan
  was not yet present under `docs/plans`.
- Green: `python3 scripts/check_watchos_contracts.py` passed after syncing the
  duplicated WatchKit controller and checking both source paths.

## Verification

- `python3 scripts/check_watchos_contracts.py`
- `make check`
- `git diff --check`
