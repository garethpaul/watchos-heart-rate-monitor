# Current Heart-Rate Query Callback Guard

Status: In Progress

## Problem

HealthKit query callbacks currently reject updates only while a workout is
inactive. A stopped query can still deliver a late callback after another
workout has started; at that point `workoutActive` is true again, so the stale
query can advance the shared anchor and display samples from the prior workout.

## Plan

1. Require both the initial anchored-query callback and update handler to match
   the controller's currently retained heart-rate query.
2. Keep the checked-in WatchKit source and UI-test mirror byte-identical.
3. Add ordered static contracts that fail if either identity guard is removed,
   weakened, or placed after anchor mutation.
4. Run the focused contract, the complete portable gate from repository and
   external working directories, and hostile mutations.

## Verification

Pending implementation and validation.
