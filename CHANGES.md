# Changes

## 2026-06-09

- Bounded displayed WatchKit heart-rate sample values before converting them to
  `UInt16` in both controller copies.
- Added mirrored static contract coverage for heart-rate display value bounds.
- Dispatched denied HealthKit authorization UI updates onto the main queue in
  both WatchKit controller copies.
- Added mirrored static contract coverage for authorization denial UI dispatch.
- Reset WatchKit workout state and ended retained sessions when heart-rate
  query creation fails.
- Added mirrored static contract coverage for heart-rate query startup failure.
- Reset WatchKit workout active state, Start button title, and retained session
  state when sessions end normally.
- Added mirrored static contract coverage for ended-session UI cleanup.
- Reset WatchKit workout UI state, stopped retained heart-rate queries, and
  avoided `error.userInfo` logging when a workout session fails.
- Added mirrored static contract coverage for failed-session UI handling.

## 2026-06-08

- Started WatchKit workouts from the local `HKWorkoutSession` value instead of
  force-unwrapping optional controller state.
- Synced the duplicated WatchKit controller with the retained-query lifecycle and guarded HealthKit anchors.
- Tightened docs-plan verification to require recorded `make check` evidence.
- Added a local `make verify` gate with static WatchKit privacy and lifecycle contract checks.
- Retained the active HealthKit heart-rate query so workout shutdown stops the same query it started.
- Guarded HealthKit update anchors before updating controller state.
- Declared HealthKit share usage descriptions in the app and WatchKit extension manifests.
