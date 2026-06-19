# Authorization Callback Generation Guard

Status: Completed

## Problem

The WatchKit controller currently rejects HealthKit authorization UI work only
while `interfaceActive` is false. If activation A requests authorization,
deactivates, and activation B begins before A's callback reaches the main
queue, the stale callback observes an active interface and can enable or deny
the Start control for the wrong activation.

## Requirements

- R1. Assign a distinct generation to every interface activation.
- R2. Capture the current generation before requesting HealthKit
  authorization.
- R3. Apply authorization callback UI work only when the interface is active
  and the captured generation still matches the current activation.
- R4. Invalidate the current generation during deactivation.
- R5. Keep the production and UI-test mirror controllers identical.
- R6. Add dependency-free, mutation-sensitive contracts for generation
  capture, comparison, invalidation, ordering, and mirror parity.

## Implementation

1. Add an integer generation property beside the existing interface
   lifecycle state in both mirrored controllers.
2. Advance and capture the generation in `willActivate()` before the
   asynchronous authorization request.
3. Advance the generation in `didDeactivate()` and require both active state
   and generation equality inside main-queue callback work.
4. Extend the portable contract checker, documentation, and hostile mutation
   gate without changing HealthKit permissions or adding dependencies.

## Verification

- The focused inactive-interface and activation-generation contracts passed for
  both mirrored controllers.
- Eight hostile source mutations covering missing state, missing increments,
  missing capture, missing comparison, off-main-queue comparison, late capture,
  deactivation invalidation, and mirror divergence were rejected.
- Final local and external-working-directory `make check` runs passed under
  explicit three-minute timeouts with 20 watchOS contracts and all 17 workflow
  mutations.
- Python syntax and mirrored source validation passed. Workflow YAML, project
  XML/plists, intended paths, generated artifacts, conflict markers,
  whitespace, and changed-line credential patterns are included in the final
  audit.
- Xcode compilation, simulator execution, and live HealthKit authorization are
  unavailable on this Linux host and are not claimed.

## Scope Boundaries

- Do not change requested HealthKit data types, workout behavior, query
  behavior, signing, deployment targets, or project structure.
- Do not merge or close any pull request without explicit owner authorization.
