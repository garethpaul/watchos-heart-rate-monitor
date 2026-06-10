# Main-Queue Stale Heart-Rate Callback

Status: Completed

## Context

HealthKit callbacks checked `workoutActive` before scheduling UI work, but a
workout could end before that block reached the main queue. The delayed block
could then display a stale heart-rate value after the interface had reset.

## Changes

- Rechecked `workoutActive` inside the main-queue heart-rate update block.
- Applied the same lifecycle guard to both checked-in WatchKit controller
  copies.
- Added static regression coverage for guard ordering.
- Rooted Make execution and fixed the hosted Linux runner and action release
  annotations.

## Verification

- `make check`
- `python3 -m py_compile scripts/check_watchos_contracts.py`
- Mutation checks for both controller copies, CI, and rooted Make execution
- `git diff --check`

Physical Apple Watch verification remains required for live HealthKit behavior.
