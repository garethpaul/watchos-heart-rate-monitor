# CI Baseline

Status: Completed

## Context

The repository had portable HealthKit and WatchKit contracts but no hosted
workflow enforced them for pushes and pull requests.

## Changes

- Added read-only static verification on Python 3.10, 3.12, and 3.14.
- Pinned actions to immutable commits and bounded job runtime.
- Extended repository contracts and maintenance docs to protect the gate.

## Verification

- `make check`
- `python3 -m py_compile scripts/check_watchos_contracts.py`
- `git diff --check`
