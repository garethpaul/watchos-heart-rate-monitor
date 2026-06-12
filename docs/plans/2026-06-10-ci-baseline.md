# CI Baseline

status: completed

## Context

The repository had a local static `make check` baseline for HealthKit privacy,
WatchKit lifecycle, workout session, and heart-rate UI guardrails, but no
hosted workflow ran it for pushes and pull requests.

## Changes

- Added a GitHub Actions workflow that installs Python 3.12 and runs
  `make check`.
- Extended the static contract checker and docs so the hosted CI path stays
  visible.

## Verification

- `make check`
