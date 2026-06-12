# Latest Heart-Rate Sample

Status: Completed

## Context

HealthKit anchored queries can deliver multiple samples in one callback. The
controllers displayed the first sample while advancing the query anchor past
the complete batch, so a newer measurement in that batch might never appear.

## Changes

- Select the last heart-rate sample from callback batches in both mirrored
  WatchKit controllers.
- Preserve the active-workout recheck before reading the batch on the main
  queue.
- Add static contracts that reject oldest-sample selection and require the
  latest-sample behavior in both project copies.

## Verification

- `make check`
- Restore `.first` in one controller and confirm the static contract fails
  before restoring `.last`.
