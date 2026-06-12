# Authorization Lifecycle Guard

Status: Completed

## Problem

`willActivate()` requests HealthKit authorization asynchronously and later
re-enables the Start button on the main queue. If the watch interface
deactivates before that callback runs, stale authorization work can mutate an
inactive controller and leave controls enabled from an obsolete activation.

## Plan

1. Track whether the interface is currently active.
2. Mark activation before requesting authorization and clear it from
   `didDeactivate()`.
3. Ignore queued authorization UI work after deactivation.
4. Keep the source and UI-test mirror controllers synchronized.
5. Extend portable lifecycle contracts and hostile mutations.

## Verification

- The focused authorization lifecycle contract passed for both mirrored
  controllers.
- `make check` passed 18 watchOS contracts and 17 workflow mutations; Xcode
  execution was explicitly skipped because this Linux host lacks xcodebuild.
- An external-working-directory Make invocation passed the same gates.
- Guard-removal, deactivation-invalidation, and mirror-divergence mutations
  were rejected.
- Python compilation and `git diff --check` passed.
