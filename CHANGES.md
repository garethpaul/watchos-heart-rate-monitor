# Changes

## 2026-06-26 03:53 PDT

- **Priority:** P1 HealthKit sample privacy and workout correctness.
- **Summary:** Scoped each heart-rate query to the workout that created it so
  an initial callback cannot display samples saved before the current workout.
- **Work:** Reset the anchored-query cursor when a workout reaches Running,
  added a strict workout-start predicate in both mirrored controllers, and
  strengthened the portable ownership and mutation contracts.
- **Threads:** No open issue or pull request covered this focused correction.
- **Files:** Updated both `InterfaceController.swift` copies, query-ownership
  contracts, project guidance, this cycle record, and a completed design plan.
- **Validation:** The test-first ownership contract failed on the reused anchor
  and missing predicate. Focused mutations, root/external `make check`, mirror
  comparison, and hosted checks are required before merge.
- **Findings:** A no-anchor anchored query returns all matching history, while
  the prior nil predicate admitted heart-rate samples from before the workout.
- **Blockers:** Native legacy WatchKit behavior still requires compatible
  macOS, Xcode, signing, and physical-device verification.
- **Next action:** Review the exact branch head and merge only after hosted
  checks pass.

## 2026-06-25 08:51 PDT

- **Priority:** P1 HealthKit privacy and authorization correctness.
- **Summary:** Corrected the sample's interpretation of HealthKit authorization
  results so it no longer claims that read-access denial is observable.
- **Work:** Renamed denial feedback to request-processing failure feedback in
  both mirrored controllers, strengthened portable contracts, updated current
  security and hardware-verification guidance, and added a completed plan.
- **Threads:** No open issue or pull request covered this focused correction.
- **Files:** Updated both `InterfaceController.swift` copies, contributor and
  project guidance, device verification, static contracts, and the new plan.
- **Validation:** The test-first contract failed against `not allowed`; focused
  contracts, a hostile semantic mutation, root and external-directory
  `make check`, mirror comparison, and `git diff --check` then passed. Native
  build execution was skipped because `xcodebuild` is unavailable.
- **Findings:** Apple's API contract says callback success reports request
  processing, not whether read permission was granted.
- **Blockers:** Native legacy WatchKit behavior still requires compatible
  macOS, Xcode, signing, and physical-device verification.
- **Next action:** Review the exact branch head and merge only after hosted
  checks pass.

## 2026-06-21

- Isolated Make verification authority from caller-controlled roots, shells,
  startup files, Makefile lists, unsafe modes, executable Make syntax, and
  later single-colon public recipe replacement.
- Added literal Python/Xcode and cleanup-containment authority coverage and
  invoked hosted verification through `/usr/bin/make`.

## 2026-06-19

- Moved anchored-query result ownership onto the main queue before workout,
  query, error, anchor, or sample state is inspected or changed.
- Retained status and source text across inactive WatchKit periods and restored
  that state plus baseline heart geometry during activation.
- Rejected zero BPM samples and relinquished ending workout sessions before
  requesting asynchronous termination.
- Added twelve hostile query-ownership mutations and mirrored lifecycle checks.

## 2026-06-17

- Generation-bound delayed heart-icon callbacks to the active interface and
  workout, and reset the icon synchronously during teardown.
- Added mirrored source contracts and fourteen hostile animation mutations.

## 2026-06-16

- Rejected delayed HealthKit callbacks unless they belong to the currently
  retained heart-rate query, preventing a stopped workout's samples from
  mutating a newly started workout, including after UI work has been queued.
- Added mirrored static contracts for query identity and anchor-update order.
- Failed closed when the current heart-rate streaming query reports an error,
  stopping and clearing query/session state before generic failure UI.

## 2026-06-14

- Added a privacy-preserving physical Apple Watch verification checklist for
  HealthKit authorization, workout start/stop, live samples, interruptions,
  relaunch behavior, redacted evidence, and unresolved failures.

## 2026-06-13

- Rejected HealthKit authorization callbacks from earlier WatchKit activation
  cycles after the interface deactivates and reactivates.
- Added mirrored generation-ordering contracts for authorization UI work.
- Stopped and cleared the retained HealthKit heart-rate query immediately when
  the user stops a workout, before requesting asynchronous session termination.
- Added mirrored lifecycle and ordering contracts for immediate query cleanup.

## 2026-06-12

- Ignored queued HealthKit authorization UI work after the WatchKit interface
  deactivates, in both source and UI-test mirror controllers.
- Added lifecycle-ordering and exact mirror-synchronization contracts.

## 2026-06-10

- Selected the newest heart-rate value from each HealthKit callback batch in
  both WatchKit controller copies instead of displaying the oldest value.
- Rechecked workout state inside queued main-thread heart-rate UI updates in
  both WatchKit controller copies so ended sessions cannot display stale data.
- Made Make execution root-independent and fixed the static CI job to Ubuntu
  24.04 with exact action release annotations.
- Kept the final bytecode cleanup root-independent when `make check` is invoked
  through an absolute Makefile path from another working directory.
- Added a pinned, read-only GitHub Actions matrix for Python 3.10, 3.12, and
  3.14 that runs the static `make check` baseline with credential-free checkout.
- Added dependency-free workflow tests that reject contradictory or relocated
  credential settings and other CI policy regressions.

## 2026-06-09

- Ignored delayed heart-rate query callbacks after workouts are inactive in
  both WatchKit controller copies.
- Added mirrored static contract coverage for inactive heart-rate callback
  guards.
- Disabled the WatchKit Start button while HealthKit authorization is
  unavailable, denied, or pending, and re-enabled it after successful
  authorization on the main queue in both controller copies.
- Added mirrored static contract coverage for HealthKit authorization
  Start-button state.
- Dispatched WatchKit workout session start/end/failure UI cleanup onto the
  main queue in both controller copies and clear retained failed sessions.
- Added mirrored static contract coverage for workout session delegate UI
  dispatch.
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
