# CI Baseline

Status: Completed

## Context

The repository had portable HealthKit and WatchKit contracts but no hosted
workflow enforced them for pushes and pull requests.

## Changes

- Added read-only static verification on Python 3.10, 3.12, and 3.14.
- Pinned actions to immutable commits and bounded job runtime.
- Disabled checkout credential persistence and added 17 dependency-free hostile
  mutations for credentials, permissions, triggers, actions, matrix coverage,
  runtime bounds, hosted Xcode, and the canonical gate.
- Made both verification and final bytecode cleanup independent of the caller's
  working directory.
- Extended repository contracts and maintenance docs to protect the gate.

## Verification

- `make check`
- `python3 -B scripts/test_workflow_contract.py`
- `python3 -B scripts/check_watchos_contracts.py`
- `make -f /path/to/watchos-heart-rate-monitor/Makefile check` from outside the repository
- `git diff --check`
