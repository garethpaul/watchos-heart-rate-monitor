# Changes

## 2026-06-08

- Tightened docs-plan verification to require recorded `make check` evidence.
- Added a local `make verify` gate with static WatchKit privacy and lifecycle contract checks.
- Retained the active HealthKit heart-rate query so workout shutdown stops the same query it started.
- Guarded HealthKit update anchors before updating controller state.
- Declared HealthKit share usage descriptions in the app and WatchKit extension manifests.
