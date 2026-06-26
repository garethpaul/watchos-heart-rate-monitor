# watchos-heart-rate-monitor

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/watchos-heart-rate-monitor` is an Apple platform application or Swift sample. HRM for WatchOS

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Swift (13).

## Repository Contents

- `HeartyMonitor` - source or example code
- `HeartyMonitor WatchKit App` - source or example code
- `HeartyMonitor WatchKit Extension` - source or example code
- `HeartyMonitor.xcodeproj` - Xcode project file
- `HeartyMonitorTests` - source or example code
- `HeartyMonitorUITests` - source or example code
- `SECURITY.md` - security reporting and disclosure guidance
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: HeartyMonitor, HeartyMonitor WatchKit App, HeartyMonitor WatchKit Extension, HeartyMonitorTests, HeartyMonitorUITests
- Dependency and build manifests: none detected
- Entry points or build surfaces: HeartyMonitor.xcodeproj
- Test-looking files: HeartyMonitorTests/HeartyMonitorTests.swift, HeartyMonitorTests/Info.plist, HeartyMonitorUITests/HeartyMonitor/AppDelegate.swift, HeartyMonitorUITests/HeartyMonitor/Assets.xcassets/AppIcon.appiconset/Contents.json, HeartyMonitorUITests/HeartyMonitor/Info.plist, HeartyMonitorUITests/HeartyMonitor/ViewController.swift, HeartyMonitorUITests/HeartyMonitor WatchKit App/Assets.xcassets/AppIcon.appiconset/Contents.json, HeartyMonitorUITests/HeartyMonitor WatchKit App/Assets.xcassets/Contents.json, and 4 more

## Getting Started

### Prerequisites

- Git
- Python 3 and Make for the portable repository checks

The checked-in project records Xcode 7.2-era metadata and uses Swift 2-era
source, with iOS 9.2 and watchOS 2.1 deployment targets. Native work therefore
requires a macOS environment capable of running the historical Xcode 7.2
toolchain and its matching SDKs, simulator runtimes, signing support, and (for
physical verification) a compatible paired iPhone and Apple Watch. That
historical environment has not been rerun as part of current maintenance, so
these prerequisites describe the project era rather than a verified supported
configuration.

The project does not currently compile with modern Xcode. Xcode 26.0.1 rejects
the project before normal source compilation because no supported
`SWIFT_VERSION` is configured; forcing Swift 5 exposes additional obsolete
WatchKit and HealthKit APIs and delegate signatures. Modernization is separate
work and is not part of the portable verification described below.

### Setup

```bash
git clone https://github.com/garethpaul/watchos-heart-rate-monitor.git
cd watchos-heart-rate-monitor
```

The setup commands above are derived from repository files.

## Running or Using the Project

To inspect the native project:

```bash
open HeartyMonitor.xcodeproj
```

In a matching historical toolchain, the repository's unsigned build command is:

```bash
/usr/bin/xcodebuild -project HeartyMonitor.xcodeproj -scheme HeartyMonitor \
  -configuration Debug CODE_SIGNING_ALLOWED=NO build
```

That command is documented for reproducibility; a successful Xcode 7.2 build
is not claimed by current maintenance. It fails with the available modern
Xcode toolchain for the compatibility reasons above. Runtime behavior still
requires an era-compatible simulator or device, and physical HealthKit
behavior requires the separate hardware matrix in `DEVICE_VERIFICATION.md`.

## Testing and Verification

- `make lint`, `make test`, `make contract-test`, and `make root-test` are the
  portable local checks. `make test` runs static source-contract checks; it
  does not invoke XCTest or validate native runtime behavior.
- To run the same complete portable boundary from any working directory while
  deliberately skipping unavailable native compilation, use:

  ```bash
  XCODEBUILD=/definitely/not-xcodebuild make -f /absolute/path/to/watchos-heart-rate-monitor/Makefile check
  ```

- GitHub Actions runs `/usr/bin/make check` on Ubuntu, where `xcodebuild` is not
  installed. Hosted success therefore validates the static repository
  contracts, workflow policy, mutation checks, Make authority boundary, and
  cleanup behavior; it does not validate compilation, XCTest, simulator use,
  Apple Watch behavior, or HealthKit behavior.
- `make verify` runs the portable checks and also attempts the unsigned Xcode
  build when the configured `XCODEBUILD` path is executable. `make check` adds
  bytecode cleanup before and after `make verify`. On a modern macOS/Xcode
  workstation, the native build is currently expected to fail.
- `make root-test` exercises every public target across hostile external paths,
  root and shell overrides, startup files, Makefile-list replacement, later
  recipe definitions, unsafe execution modes, and literal Python/Xcode paths.
- Repository verification derives its root and shell from the reviewed
  `Makefile`, accepts literal `PYTHON` and `XCODEBUILD` paths, and rejects
  injected startup files and non-executing or error-ignoring Make modes.
  Hosted checks invoke `/usr/bin/make` explicitly.
- `python3 scripts/check_watchos_contracts.py` runs the HealthKit privacy,
  entitlement, plan, query-lifecycle, authorization request-error UI-thread,
  authorization request Start-button state, session-start, workout delegate UI-thread,
  query-start failure, inactive and queued stale heart-rate callbacks,
  activation-generation authorization guards, immediate query-stop,
  main-queue query ownership, current-query error cleanup, generation-bound
  heart animation, heart-rate value-bound, and workout
  session-failure/session-end contracts.
- Start remains disabled while the HealthKit authorization request is pending,
  becomes enabled after the request is processed successfully, and remains
  disabled with `authorization failed` feedback when request processing fails.
  HealthKit does not reveal read-access grant or denial through this callback.
- Heart-rate query errors stop and clear the current query and workout, restore
  the Start state, and use a generic failure message without exposing details.
- Delayed heart-icon callbacks recheck interface, workout, and animation
  generation state; teardown paths invalidate queued work and restore the
  default icon size synchronously.
- Anchored-query callbacks enter the main queue before checking query identity
  or advancing the shared anchor. Each workout resets that anchor and applies a
  strict workout-start predicate so the initial callback cannot display older
  heart-rate samples. Status and source text are retained while the interface
  is inactive and restored during the next activation.
- Completed maintenance plans live under `docs/plans` and are checked by
  `make check`.
- See `docs/plans/2026-06-21-make-authority-isolation.md` for the consolidated
  Make, Python, Xcode, recipe-replacement, and cleanup-containment boundary.
- GitHub Actions runs the static contracts on Python 3.10, 3.12, and 3.14
  on Ubuntu 24.04 with read-only permissions, credential-free checkout,
  immutable action pins, and cancellation for superseded runs. Dependency-free
  mutations reject contradictory credential settings and policy regressions.
- `HeartyMonitorTests` and `HeartyMonitorUITests` are generated XCTest
  templates. Their example and performance methods contain no assertions, and
  launching the app in UI-test setup is not meaningful behavioral coverage.
  Current maintenance therefore does not claim native test coverage from
  those targets.
- `DEVICE_VERIFICATION.md` defines the required physical Apple Watch and
  HealthKit authorization, workout, live-sample, stop, interruption, privacy,
  and redacted evidence checks. Its execution status remains explicit until a
  reviewer performs the matrix on hardware.

When the historical SDK or runtime is unavailable, use the portable commands
and source review without treating them as evidence of native behavior. Any
future native claim must identify the exact working toolchain and complete the
appropriate simulator or physical-device verification separately.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.
- HealthKit read access uses `NSHealthShareUsageDescription` to explain that the sample reads heart-rate data for live workout feedback.

## Security and Privacy Notes

- Review changes touching network requests, sockets, or service endpoints; examples from the scan include HeartyMonitor/Info.plist, HeartyMonitor WatchKit App/Info.plist, HeartyMonitor WatchKit Extension/Info.plist, HeartyMonitorTests/Info.plist, and 5 more.
- Review changes touching mobile permissions or privacy-sensitive device data; examples from the scan include HeartyMonitor/AppDelegate.swift, HeartyMonitor/Info.plist, HeartyMonitor WatchKit Extension/Info.plist, HeartyMonitor WatchKit Extension/InterfaceController.swift, and 4 more.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include HeartyMonitor/Info.plist, HeartyMonitor WatchKit App/Info.plist, HeartyMonitor WatchKit Extension/Info.plist, HeartyMonitorTests/Info.plist, and 5 more.

## Maintenance Notes

- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-healthkit-privacy-strings.md` for the current
  HealthKit privacy and query baseline.
- See `docs/plans/2026-06-08-watchkit-uitest-query-mirror.md` for the duplicated
  WatchKit controller lifecycle mirror.
- See `docs/plans/2026-06-08-watchkit-session-start.md` for non-forced workout
  session startup in the app and UI-test mirror.
- See `docs/plans/2026-06-09-watchkit-session-failure-ui.md` for mirrored
  failed-session UI and non-sensitive logging coverage.
- See `docs/plans/2026-06-09-watchkit-session-end-ui.md` for mirrored normal
  ended-session UI cleanup.
- See `docs/plans/2026-06-09-watchkit-authorization-main-thread.md` for
  the historical mirrored HealthKit authorization callback UI dispatch change.
- See `docs/plans/2026-06-09-watchkit-authorization-start-button.md` for
  the historical mirrored HealthKit authorization Start-button change.
- See `docs/plans/2026-06-25-healthkit-authorization-result-semantics.md` for
  the current request-processing semantics and read-authorization boundary.
- See `docs/plans/2026-06-09-watchkit-query-start-failure-ui.md` for mirrored
  cleanup when heart-rate streaming query creation fails.
- See `docs/plans/2026-06-09-watchkit-heart-rate-value-bounds.md` for mirrored
  bounds checks before heart-rate values are converted for display.
- See `docs/plans/2026-06-09-watchkit-session-delegate-main-thread.md` for
  mirrored workout session delegate UI dispatch coverage.
- See `docs/plans/2026-06-09-watchkit-inactive-heart-rate-callbacks.md` for
  mirrored guards that ignore heart-rate callbacks after workouts are inactive.
- See `docs/plans/2026-06-10-ci-baseline.md` for hosted static verification.
- See `docs/plans/2026-06-10-main-queue-stale-heart-rate-callback.md` for the
  mirrored guard against UI updates queued before a workout ends.
- See `docs/plans/2026-06-10-latest-heart-rate-sample.md` for mirrored
  latest-sample selection when HealthKit delivers callback batches.
- See `docs/plans/2026-06-12-authorization-lifecycle-guard.md` for the mirrored
  guard against stale authorization UI work after interface deactivation.
- See `docs/plans/2026-06-13-authorization-callback-generation.md` for rejecting
  authorization callbacks captured by an earlier interface activation.
- See `docs/plans/2026-06-13-stale-workout-session-callbacks.md` for rejecting
  obsolete session callbacks and late workout starts on the main queue.
- See `docs/plans/2026-06-13-watchkit-immediate-query-stop.md` for stopping and
  clearing the retained heart-rate query before workout-session termination.
- See `docs/plans/2026-06-14-device-verification-checklist.md` for the physical
  Apple Watch verification and evidence contract.
- See `docs/plans/2026-06-16-heart-rate-query-error.md` for fail-closed current
  query error handling and mirrored controller coverage.
- See `docs/plans/2026-06-19-watchos-main-queue-query-ownership.md` for
  main-queue anchor ownership, inactive interface restoration, and explicit
  workout-stop ownership.
- See `docs/plans/2026-06-26-workout-sample-admission.md` for per-workout anchor
  reset and strict start-date sample admission.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
