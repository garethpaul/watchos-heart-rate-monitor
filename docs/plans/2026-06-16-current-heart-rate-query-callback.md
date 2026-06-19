# Current Heart-Rate Query Callback Guard

Status: Completed

## Problem

HealthKit query callbacks currently reject updates only while a workout is
inactive. A stopped query can still deliver a late callback after another
workout has started; at that point `workoutActive` is true again, so the stale
query can advance the shared anchor and display samples from the prior workout.

## Plan

1. Require both the initial anchored-query callback and update handler to match
   the controller's currently retained heart-rate query.
2. Carry callback query identity into queued main-thread UI work and recheck it
   before reading or displaying samples.
3. Keep the checked-in WatchKit source and UI-test mirror byte-identical.
4. Add ordered static contracts that fail if any identity guard is removed,
   weakened, or placed after anchor mutation.
5. Run the focused contract, the complete portable gate from repository and
   external working directories, and hostile mutations.

## Verification

- The focused current-query callback contract passed for both mirrored
  controllers, and the controller files remained byte-identical.
- `make check` passed 22 watchOS contracts and 17 workflow mutations; Xcode
  execution was explicitly skipped because this Linux host lacks xcodebuild.
- An external-working-directory Make invocation passed the same complete gate.
- Initial-guard removal, update-guard removal, queued-guard removal, post-anchor
  guard ordering, contract deregistration, mirror divergence, and
  incomplete-plan mutations were all rejected.
