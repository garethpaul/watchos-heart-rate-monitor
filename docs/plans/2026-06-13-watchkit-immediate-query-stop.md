# Immediate Heart-Rate Query Stop

Status: Completed

## Problem

Tapping Stop marks the workout inactive and requests the workout session to
end, but the retained heart-rate query is not stopped until the asynchronous
`.Ended` delegate callback. A user can start another workout before that
callback arrives, replacing the query reference while the older query remains
executing without a retained handle.

## Plan

1. Stop and clear the retained heart-rate query immediately when the active
   workout is stopped.
2. Keep normal session-end and failure cleanup idempotent.
3. Keep the source and UI-test mirror controllers synchronized.
4. Extend the portable contracts to require query cleanup before requesting
   workout-session termination.
5. Document the lifecycle guarantee and completed verification.

## Verification

- The focused immediate-query-stop contract passed.
- The full `make check` gate passed locally and from an external working
  directory with all 19 watchOS contracts and all 17 workflow mutations.
- Five hostile source mutations were rejected for missing cleanup, reversed
  ordering, missing query clearing, mirror divergence, and stale plan status.
- Python compilation and `git diff --check` passed.
- Xcode execution was explicitly skipped because this Linux host does not
  provide `xcodebuild`.
