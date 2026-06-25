# HealthKit Authorization Result Semantics

## Status: Completed

## Context

`HKHealthStore.requestAuthorizationToShareTypes` reports whether the
authorization request was processed. Apple documents that a successful callback
does not indicate whether the user granted read permission. The sample instead
treated callback failure as an observable read denial and displayed `not
allowed`, which overstated information that HealthKit intentionally keeps
private.

Apple reference:
<https://developer.apple.com/documentation/healthkit/hkhealthstore/requestauthorization%28toshare%3Aread%3Acompletion%3A%29>

## Objectives

- Keep Start disabled while authorization request processing is pending.
- Enable Start after the authorization request is processed successfully.
- Keep Start disabled and show request-failure feedback when processing fails.
- Avoid claiming that the callback reveals read-access grant or denial.
- Keep the app controller and UI-test mirror synchronized.

## Work Completed

- Replaced read-denial feedback with `authorization failed` request-processing
  feedback in both controller copies.
- Added static contracts that reject the obsolete `not allowed` claim.
- Updated current security, vision, verification, and contributor guidance.
- Preserved historical plans and change records as records of their original
  implementation context.

## Test-First Evidence

- Updated the authorization contract before production code; it failed because
  the controllers still displayed `not allowed`.
- Updated both mirrored controllers; the focused contract suite then passed.

## Verification

- `python3 scripts/check_watchos_contracts.py`
- `python3 scripts/test_heart_animation_generation_contract.py`
- `python3 scripts/test_heart_rate_query_ownership_contract.py`
- `make check`
- external-directory `make check`
- hostile authorization-semantic mutation
- `git diff --check`

The native legacy WatchKit build remains a separate macOS/Xcode validation
boundary and is not claimed by portable static verification.
