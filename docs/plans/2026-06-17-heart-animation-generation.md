# Heart Animation Generation

## Status: Completed

## Priority

1. Prevent delayed heart-icon callbacks from overriding newer heartbeat animations.
2. Prevent queued animation work from mutating inactive or stopped workout UI.
3. Restore the default heart size synchronously during every workout teardown path.
4. Enforce mirrored source and ordering behavior with portable mutation tests.

## Context

`animateHeart` expands the icon and schedules an unconditional shrink after
half a second. Faster samples can queue several overlapping callbacks, and an
older callback can run after a newer beat, interface deactivation, or workout
cleanup. The delayed callback currently has no ownership or lifecycle check.

## Requirements

- R1. Retain a monotonically increasing heart-animation generation.
- R2. Require active interface and workout ownership, then capture the current
  generation before starting each expansion.
- R3. Recheck interface activity, workout activity, and generation ownership on
  the main queue before applying a delayed shrink.
- R4. Invalidate queued callbacks and restore the default icon size during
  interface deactivation and every workout/query teardown path.
- R5. Keep the canonical and UI-test mirror controllers synchronized.
- R6. Add a focused contract, hostile mutations, and maintenance guidance.

## Implementation Units

### U1. Generation-bind delayed animation work

**Files:** `HeartyMonitor WatchKit Extension/InterfaceController.swift`,
`HeartyMonitorUITests/HeartyMonitor WatchKit Extension/InterfaceController.swift`

Add generation state, a shared reset operation, and delayed-callback guards.
Use the reset operation from interface, session, query, and user-stop cleanup.

### U2. Enforce animation ownership

**Files:** `scripts/heart_animation_generation_contract.py`,
`scripts/test_heart_animation_generation_contract.py`,
`scripts/check_watchos_contracts.py`, `Makefile`

Require generation/reset ordering in both controller copies and reject focused
mutations that remove lifecycle resets or delayed-callback guards.

### U3. Record the animation boundary

**Files:** `AGENTS.md`, `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`,
`docs/plans/2026-06-17-heart-animation-generation.md`

Document that delayed heart animations are lifecycle- and generation-bound.

## Verification Plan

- Run the focused mutation suite.
- Run repository-root and external-directory `make check` with hard timeouts.
- Compile Python checkers and audit the intended diff, generated artifacts,
  conflict markers, file modes, large files, and credential-like additions.
- Capture one bounded exact-head hosted and security snapshot after push.

## Scope Boundaries

- Do not change HealthKit query/session behavior, sample selection, value
  bounds, animation dimensions, durations, or the device verification matrix.
- Do not modernize Swift, WatchKit, or HealthKit APIs.
- Do not claim native watchOS runtime coverage from Linux.

## Work Completed

- Generation-bound heart expansion and delayed shrink work to the current
  interface and workout lifecycle.
- Added a shared reset that invalidates queued callbacks and restores the
  default icon size across interface, session, query, and user-stop teardown.
- Kept the canonical and UI-test mirror controllers synchronized.
- Added a reusable contract, fourteen hostile mutations, canonical Make
  integration, and synchronized maintenance guidance.

## Verification Completed

- The focused heart-animation generation contract rejected fourteen lifecycle,
  reset, ordering, ownership, and generation mutations.
- Repository and external-directory `make check` passed the canonical static
  and workflow gates; Linux truthfully skipped Xcode because `xcodebuild` is
  unavailable.
- Python compilation, exact-diff, generated-artifact, conflict-marker,
  file-size, file-mode, and added-line credential audits passed.
- No simulator, Apple Watch, HealthKit stream, or animation timing behavior was
  exercised on this Linux host.
