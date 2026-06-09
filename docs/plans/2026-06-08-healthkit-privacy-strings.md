# HealthKit Privacy And Query Contracts Plan

Date: 2026-06-08

Status: Completed

## Goal

Make the sample's HealthKit permission boundary explicit and lock in safer heart-rate query lifecycle behavior.

## Scope

- Add `NSHealthShareUsageDescription` to the iOS app and WatchKit extension `Info.plist` files.
- Keep the duplicated sample project under `HeartyMonitorUITests/` in sync with the top-level project.
- Add a dependency-free contract script and Makefile targets that can run without Xcode.
- Preserve the existing HealthKit entitlement, read-only authorization flow, retained active query, and guarded query anchor handling.

## TDD Notes

- Red: `python3 scripts/check_watchos_contracts.py` failed with `AssertionError: HeartyMonitor/Info.plist must declare NSHealthShareUsageDescription`.
- Green: `python3 scripts/check_watchos_contracts.py` passed after adding the HealthKit share usage descriptions, retained-query check, and guarded-anchor check.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `make check`
- `git diff --check`
- Xcode build is skipped in this environment because `xcodebuild` is not installed.
