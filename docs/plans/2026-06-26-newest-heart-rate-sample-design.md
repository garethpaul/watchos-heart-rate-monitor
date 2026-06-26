# Newest Heart-Rate Sample Selection Design

## Context

The WatchKit controller currently displays `heartRateSamples.last` when an
anchored HealthKit query returns a batch. Apple documents the callback value as
an array of matching added samples and the anchor as the last returned object,
but does not document chronological ordering for the array. Treating its final
position as the newest measurement can therefore display an older sample while
advancing the anchor past the full batch.

Primary reference:
<https://developer.apple.com/documentation/healthkit/hkanchoredobjectquery>

## Options Considered

1. Keep `.last` and rely on observed HealthKit ordering. This is smallest but
   relies on an undocumented property and preserves the stale-display risk.
2. Sort the whole batch by `startDate`. This is correct but allocates and orders
   every sample when only one maximum is needed.
3. Scan once for the greatest `startDate`. This is linear, allocation-free,
   compatible with the legacy controller shape, and explicit about the desired
   behavior.

## Decision

Use option 3 in both the app controller and the UI-test mirror. Start from the
first typed sample, compare each remaining sample's `startDate`, and retain the
candidate whose date is later. Preserve existing workout/query identity guards,
value bounds, source display, and heart animation behavior.

## Verification

- Change the static contract first to reject positional `.last` selection and
  require a start-date maximum scan in both mirrored controllers.
- Observe the contract fail against the current source.
- Apply the minimal mirrored Swift change and rerun all portable contracts.
- Mutate the comparison direction, restore `.last`, remove one mirrored change,
  and weaken documentation in isolated copies; each must fail.
- Require hosted static matrix and CodeQL on the exact reviewed head before
  merge. Native watchOS runtime behavior remains a documented device boundary.
