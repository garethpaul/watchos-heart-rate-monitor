# Apple Watch Device Verification

## Execution Status

Execution status: Not yet executed. This checklist requires real watch hardware
with HealthKit heart-rate access and cannot be completed by Linux static CI or
a simulator-only review.

## Prerequisites

- A physical Apple Watch paired with an iPhone and capable of reporting heart
  rate during a workout.
- A macOS workstation with the Xcode version used for the test.
- A development team and signing configuration that can install the app on the
  paired watch without committing signing identities or provisioning data.
- HealthKit enabled for the app and WatchKit extension targets.
- A clean install or reset permission state for the first-run authorization
  checks.

Do not record raw heart-rate values, Health app exports, device identifiers,
Apple IDs, signing identities, provisioning profiles, or unredacted screenshots.

## Device Test Matrix

Run every step on the same build unless the step explicitly requires a clean
install or relaunch.

1. **First launch:** Install and launch the watch app. Confirm the HealthKit
   authorization prompt explains heart-rate read access and the Start control is
   disabled while authorization is pending.
2. **Denied access:** On a clean permission state, deny heart-rate read access.
   Confirm the label shows `not allowed`, Start stays disabled, and no workout or
   heart-rate update begins.
3. **Approved access:** Grant heart-rate read access in system settings, then
   relaunch the app. Confirm Start becomes enabled without exposing prior health
   samples.
4. **Workout start:** Tap Start. Confirm the button title changes from `Start` to
   `Stop`, a workout begins, the heart-rate label updates, the sample source label
   identifies the active source, and the heart image animates.
5. **Workout stop:** Tap Stop. Confirm the button title returns to `Start`, the
   heart-rate query stops, and the heart-rate label returns to `---` when the
   workout session ends. Wait long enough to confirm late samples do not update
   the stopped UI.
6. **Interruption and recovery:** Start another workout, interrupt the workout
   session by leaving or terminating the app, then relaunch. Confirm stale
   callbacks do not restore an obsolete workout and a new workout can start and
   stop normally.
7. **Repeatability:** Repeat start and stop once more. Confirm authorization is
   not requested unnecessarily and the displayed source and controls remain
   consistent.

## Evidence Record

Record the watch model, watchOS version, paired iPhone iOS version, Xcode
version, commit SHA, review date, reviewer, and pass/fail result for each matrix
step. Attach only redacted pass/fail evidence. A written observation is
sufficient when a screenshot would expose health or device data.

Record failures with the step, expected result, observed result, and a minimal
reproduction. Unresolved failures block merge for changes that affect HealthKit
authorization, workout lifecycle, heart-rate queries, or device UI behavior.
