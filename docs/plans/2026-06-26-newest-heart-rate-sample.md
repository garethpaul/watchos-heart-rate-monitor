# Newest Heart-Rate Sample Selection Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Display the chronologically newest heart-rate sample in every HealthKit callback batch without relying on array position.

**Architecture:** Preserve both mirrored legacy WatchKit controllers and their existing query ownership. Replace positional `.last` selection with one linear `startDate` maximum scan, then enforce that behavior through the portable Python contract and synchronized guidance.

**Tech Stack:** Swift 2-era WatchKit/HealthKit source, Python 3 static contracts, GNU Make, GitHub Actions

---

status: completed

### Task 1: Write The Failing Contract

**Files:**
- Modify: `scripts/check_watchos_contracts.py`

**Step 1: Require chronological selection**

Reject `heartRateSamples.last` and require a first-sample seed, iteration over
remaining samples, `startDate.compare`, and `.OrderedDescending` replacement in
both mirrored controllers.

**Step 2: Verify red**

Run: `python3 scripts/check_watchos_contracts.py`

Expected: FAIL because both controllers still use positional `.last`.

### Task 2: Implement The Minimal Mirrored Fix

**Files:**
- Modify: `HeartyMonitor WatchKit Extension/InterfaceController.swift`
- Modify: `HeartyMonitorUITests/HeartyMonitor WatchKit Extension/InterfaceController.swift`

**Step 1: Seed the newest candidate**

Guard the first typed sample and store it in a mutable local.

**Step 2: Scan remaining samples**

Replace the candidate only when another sample's `startDate` compares as
`.OrderedDescending`.

**Step 3: Verify green**

Run: `python3 scripts/check_watchos_contracts.py`

Expected: PASS.

### Task 3: Synchronize Guidance And Evidence

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `SECURITY.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-26-newest-heart-rate-sample.md`

Document that batch selection uses the greatest sample start date rather than
callback order, record exact verification, and mark the plan completed.

### Task 4: Validate And Mutate

Run every Make target from repository and external roots, then prove isolated
mutations for positional selection, reversed comparison, mirror drift, and
guidance drift are rejected.

### Task 5: Review And Merge

Push a focused PR, invoke Codex branch review, wait for all hosted checks, verify
the immutable head and clean merge state, then squash-merge with
`--match-head-commit`.

## Verification Completed

- Red-first `python3 scripts/check_watchos_contracts.py` failed because both
  controllers still selected `heartRateSamples.last`.
- The focused source contract and query-ownership mutation suite passed after
  the mirrored one-pass maximum scan was implemented.
- Root and external-directory `make check` runs and all seven Make aliases
  passed; the build target truthfully skipped because `xcodebuild` is not
  installed.
- Four isolated hostile mutations cover positional selection, reversed date
  comparison, mirror drift, and guidance drift.
- Compatible Xcode and physical Apple Watch behavior remain the documented
  native validation boundary.
