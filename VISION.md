## watchOS Heart Rate Monitor Vision

watchOS Heart Rate Monitor is a WatchKit and HealthKit sample that starts a
workout session, streams heart-rate samples, displays the current value, shows
the sample source, and animates a heart image.

The repository is useful as a focused HealthKit/watchOS learning project for
authorization, workout sessions, anchored queries, and live UI updates.

The goal is to preserve the sample while making health-data permission and
privacy boundaries explicit.

The current focus is:

Priority:

- Preserve the start/stop workout and heart-rate streaming flow
- Keep HealthKit authorization visible
- Keep HealthKit authorization UI updates on the main queue
- Keep Start disabled until HealthKit authorization allows workouts
- Keep WatchKit workout session delegate UI cleanup on the main queue
- Avoid force-unwrapping workout session state while starting workouts
- Reset visible workout controls when heart-rate query startup fails
- Reset visible workout controls when workout sessions fail
- Reset visible workout controls when workout sessions end normally
- Ignore heart-rate callbacks after workouts are inactive
- Recheck workout state before queued heart-rate UI updates
- Ignore out-of-range heart-rate values before display conversion
- Avoid storing or uploading heart-rate samples by default
- Keep GitHub Actions running the static `make check` baseline
- Treat Swift/watchOS project versions as legacy until documented

Next priorities:

- Add README setup notes for HealthKit entitlements and watchOS versions
- Add manual verification notes for device testing
- Modernize HealthKit APIs in a dedicated pass

Contribution rules:

- One PR = one focused HealthKit, workout, UI, entitlement, or documentation change.
- Do not commit health data or device identifiers.
- Keep data collection local unless a privacy model is added.
- Include watch hardware notes for runtime changes.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Heart-rate data is sensitive health information. The app should keep samples
local, request only needed permissions, and make any storage or sharing behavior
explicit before it is added.

## What We Will Not Merge (For Now)

- Silent health-data storage or upload
- Broad health analytics without a privacy model
- Entitlement changes without documentation
- Device-data fixtures from real users

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
