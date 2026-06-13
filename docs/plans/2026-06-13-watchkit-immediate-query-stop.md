# Immediate Heart-Rate Query Stop

Status: In Progress

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

- Run the focused watchOS contract.
- Run the full `make check` gate locally and from an external working
  directory.
- Reject hostile mutations for missing cleanup, reversed ordering, missing
  query clearing, mirror divergence, and stale plan status.
- Run Python compilation and `git diff --check`.
- Record Xcode availability without claiming Apple-platform execution when it
  is unavailable.
