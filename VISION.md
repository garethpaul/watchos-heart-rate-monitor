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
- Avoid storing or uploading heart-rate samples by default
- Treat Swift/watchOS project versions as legacy until documented

Next priorities:

- Add README setup notes for HealthKit entitlements and watchOS versions
- Add error handling for unavailable health data and failed sessions
- Add manual verification notes for device testing
- Modernize HealthKit APIs in a dedicated pass

Contribution rules:

- One PR = one focused HealthKit, workout, UI, entitlement, or documentation change.
- Do not commit health data or device identifiers.
- Keep data collection local unless a privacy model is added.
- Include watch hardware notes for runtime changes.

## Security And Responsible Use

Heart-rate data is sensitive health information. The app should keep samples
local, request only needed permissions, and make any storage or sharing behavior
explicit before it is added.

## What We Will Not Merge For Now

- Silent health-data storage or upload
- Broad health analytics without a privacy model
- Entitlement changes without documentation
- Device-data fixtures from real users
