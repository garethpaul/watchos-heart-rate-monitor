# Main-Queue HealthKit Query Ownership

Status: Completed

## Problem

`HKAnchoredObjectQuery` invokes its result and update handlers on a background
queue. The handlers checked `workoutActive` and query identity, then advanced
the controller's shared anchor before entering the main queue. A stopped query
could therefore pass those checks, race a main-thread stop/restart, and advance
the anchor retained for a later workout.

WatchKit also ignores interface-object changes after `didDeactivate()`. Session
or query callbacks received while inactive could update controller state while
their label, button, device, and animation changes were discarded, leaving a
stale interface after reactivation.

## Changes

- Route both HealthKit query callbacks directly to one synchronous main-queue
  result owner before reading or mutating controller state.
- Validate workout and query identity before error handling, anchor advancement,
  sample conversion, or UI state changes.
- Persist status and device text independently from WatchKit interface objects,
  then restore that state and baseline heart geometry during activation.
- Reject zero, negative, nonfinite, and over-300 BPM values before conversion.
- Relinquish workout-session ownership before explicitly ending a stopped
  session so late callbacks cannot re-enter completed stop state.
- Keep the production and UI-test mirror controllers byte-identical.

## Verification

- Focused RED/GREEN query-ownership contract.
- Twelve hostile mutations covering callback dispatch, query identity, anchor
  ordering, inactive UI state, invalid samples, activation restoration, and
  explicit-stop ownership.
- Existing animation and workflow mutation suites.
- `make check` portable payload on Python 3.10, 3.12, and 3.14, including an
  external-working-directory invocation.
- `git diff --check` and exact mirror comparison.

The installed Xcode 26 toolchain cannot compile the archival project because
its Swift 2-era language setting is unsupported. HealthKit delivery, workout
callbacks, background execution, animation timing, and reactivation still
require the physical Apple Watch matrix.
