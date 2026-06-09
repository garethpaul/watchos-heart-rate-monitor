# WatchKit Heart-Rate Value Bounds

## Status: Completed

## Context

The WatchKit controller receives heart-rate samples from HealthKit, converts the
first sample to beats per minute, and displays it by converting the value to
`UInt16`. The sample already guards missing sample arrays, but it did not bound
the numeric value before the integer conversion.

## Objectives

- Preserve live heart-rate display for normal sample values.
- Ignore negative, non-finite, or implausibly high values before display.
- Keep the app controller and UI-test fixture controller in sync.
- Extend static checks so value bounds stay before `UInt16` conversion.

## Work Completed

- Added a `0...300` value guard before the displayed `UInt16` conversion in the
  WatchKit extension controller.
- Mirrored the same guard in the duplicated UI-test fixture controller.
- Extended `scripts/check_watchos_contracts.py` with mirrored value-bound
  coverage.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_watchos_contracts.py`
- `make check`
- `git diff --check`

## Xcode Notes

`xcodebuild` was unavailable on this host, so simulator compilation was not run
here. The repository `make check` wrapper still runs the Xcode build when
`xcodebuild` is available locally.

## Follow-Up Candidates

- Add manual watch hardware verification notes for unusual HealthKit samples.
- Modernize HealthKit APIs in a dedicated compatibility pass.
