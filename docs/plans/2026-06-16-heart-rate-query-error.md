# Fail Closed When Heart-Rate Streaming Queries Error

## Status: Planned

## Context

Both HealthKit anchored-query callbacks receive an error value but currently
ignore it. If streaming fails after a workout starts, the controller can remain
in the active state with a retained query, a `Stop` button, and stale heart-rate
UI even though no further samples can be trusted.

## Requirements

- Handle initial and update-handler query errors before anchor or sample
  processing.
- Accept failures only from the currently retained query and active workout.
- Stop and clear the failed query, end and clear the current workout session,
  restore the Start control, and show the existing non-sensitive failure text.
- Dispatch visible UI changes to the main queue without exposing HealthKit
  error details or heart-rate data.
- Keep the production and UI-test mirror controllers byte-identical.
- Preserve successful sample ordering, current-query identity guards, value
  bounds, and normal stop/end behavior.
- Add mutation-sensitive portable coverage and maintained documentation.

## Implementation Units

### U1. Centralize query failure cleanup

- **Files:** `HeartyMonitor WatchKit Extension/InterfaceController.swift`,
  `HeartyMonitorUITests/HeartyMonitor WatchKit Extension/InterfaceController.swift`
- Add one current-query failure transition and route both HealthKit callback
  error paths through it.

### U2. Add portable contracts

- **Files:** `scripts/check_watchos_contracts.py`
- Verify guard ordering, main-queue cleanup, query/session invalidation,
  non-sensitive UI/logging, mirror parity, checker registration, and plan
  completion.

### U3. Maintain guidance

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Document fail-closed streaming behavior and the physical-device boundary.

## Verification

- Run the focused query-error contract plus repository and external-directory
  non-cleaning `make verify` gates with explicit timeouts.
- Reject mutations that ignore either callback error, process anchors first,
  retain failed query/session state, expose error details, diverge the mirror,
  unregister coverage, weaken guidance, or reopen the plan.
- Audit the exact diff, generated artifacts, file modes, conflicts, and
  credential-like additions before committing.

## Runtime Boundary

Local Xcode, HealthKit execution, and physical Apple Watch validation are not
available on this Linux host. Hosted portable checks and the existing device
matrix remain the authoritative follow-up boundaries.
