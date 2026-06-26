# Workout Sample Admission

Status: Completed

## Problem

The sample reused its last anchored-query cursor across workouts and supplied
no sample predicate. HealthKit anchored queries take a snapshot of all matching
objects after the supplied anchor, so a newly started workout could initially
display a heart-rate sample saved before that workout.

## Decision

- Reset the query anchor to `HKAnchoredObjectQueryNoAnchor` when the retained
  workout session reports that it is running.
- Build the query with a strict start-date predicate using the workout's start
  date.
- Preserve main-queue callback ownership, current-query identity checks, and
  anchor advancement for the lifetime of that query.
- Apply the same behavior to the app and UI-test mirror controllers.

## Verification

- The query-ownership contract requires anchor reset before query creation and
  a strict start-date predicate before the anchored query is initialized.
- Hostile mutations remove each boundary and must be rejected.
- `make check` remains the canonical portable verification gate; compatible
  Xcode and physical Apple Watch verification remain required for runtime
  HealthKit behavior.
