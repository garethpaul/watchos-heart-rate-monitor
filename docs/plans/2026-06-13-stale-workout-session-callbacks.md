# Stale Workout Session Callbacks

Status: Completed

## Problem

Workout-session delegate callbacks are queued onto the main thread before they
mutate UI and query state. A callback from a replaced session can therefore
arrive after a newer session is retained, and a late `.Running` callback can
arrive after the user has already stopped the workout.

## Plan

1. Require queued state and failure callbacks to match the retained workout
   session before changing controller state.
2. Require `.Running` callbacks to observe an active workout before starting
   the heart-rate query.
3. Keep the source and UI-test mirror controllers synchronized.
4. Extend the portable contract and reject guard-removal and ordering
   mutations.

## Verification

- The focused contract and full `make check` gate passed all 18 watchOS
  contracts and rejected all 17 workflow mutations.
- The same complete gate passed from an external working directory.
- Five hostile source mutations were rejected: state-session guard removal,
  active-workout guard removal, failure-session guard removal, late guard
  ordering, and mirror divergence.
- Python compilation and `git diff --check` passed.
- Xcode execution was explicitly skipped because this Linux host does not
  provide `xcodebuild`.
