# Apple Watch Device Verification Checklist

## Status: Completed

## Context

The repository has extensive static contracts for HealthKit authorization,
workout sessions, heart-rate queries, callback lifecycle, and UI state. It does
not define the evidence required to verify those boundaries on a physical Apple
Watch, where HealthKit permissions and live sensor data are available.

## Requirements

- Document prerequisites without recording signing identities, device
  identifiers, health samples, or screenshots containing private data.
- Verify first-run authorization, denial, later approval, workout start, live
  heart-rate/source display, stop behavior, interruption recovery, and relaunch.
- Require expected UI and privacy outcomes for every step.
- Record the watch model, watchOS version, Xcode version, review date, commands,
  and redacted pass/fail evidence.
- Keep the checklist explicitly unexecuted until a reviewer performs it on a
  physical watch.
- Link the checklist from the README and roadmap and protect it with static
  contracts and hostile mutations.

## Verification Plan

- focused device-checklist and completed-plan contracts
- repository and external-directory `make check`
- hostile prerequisite, privacy, authorization, workout, live-sample, stop,
  interruption, denial, evidence, roadmap, suite, and plan-status mutations
- final artifact, credential, exact-diff, and hosted verification audits

## Scope Boundary

- Do not change Swift behavior, Xcode project settings, entitlements, privacy
  strings, workflows, signing, or deployment targets.
- Do not claim simulator or physical-device execution from this Linux host.
- Do not merge or close stacked pull requests without owner authorization.

## Work Completed

- Added a privacy-preserving physical-device matrix with explicit HealthKit,
  workout, live-sample, stop, interruption, relaunch, and evidence outcomes.
- Linked the checklist from repository guidance and made its scope, execution
  status, roadmap priority, and completed plan mutation-sensitive.

## Verification

- Focused device-checklist and completed-plan contracts passed.
- Repository and external-directory `make check` passed; Xcode correctly
  remained unavailable on Linux.
- Twelve hostile checklist mutations were rejected across physical-device
  scope, privacy, authorization, workout, live samples, stop, interruption,
  evidence, roadmap, suite registration, and plan status.
- Final artifact, credential, and exact-diff audits passed. Hosted verification
  is recorded against the exact pull-request head after push.
