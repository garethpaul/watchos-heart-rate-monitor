# HealthKit Setup Guide Implementation Plan

Status: Completed

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Complete the README setup roadmap item with exact HealthKit entitlement, privacy-string, target, and historical watchOS configuration guidance.

**Architecture:** Derive every claim from checked-in entitlements, Info.plists, project settings, and the existing device checklist. Add a static README contract so target paths and the no-signing-secrets boundary cannot drift silently.

**Tech Stack:** Markdown, Python 3, plist/project metadata, GNU Make.

---

### Task 1: Add the failing documentation contract

**Files:**
- Modify: `scripts/check_watchos_contracts.py`

Require README to identify the app and WatchKit extension entitlement files, `com.apple.developer.healthkit`, `NSHealthShareUsageDescription`, the historical iOS 9.2/watchOS 2.1 targets, and the rule against committing signing material.

Run `python3 scripts/check_watchos_contracts.py`; expect failure because README lacks the dedicated HealthKit target-configuration section.

### Task 2: Add source-backed setup guidance

**Files:**
- Modify: `README.md`

Add a `HealthKit Target Configuration` section explaining the checked-in entitlement files, extension privacy string, project-era targets, signing/team requirement, and the separation between repository configuration and private provisioning assets.

Run `python3 scripts/check_watchos_contracts.py`; expect success.

### Task 3: Close the stale roadmap item

**Files:**
- Modify: `VISION.md`
- Modify: `CHANGES.md`
- Modify: `AGENTS.md`

Remove the completed setup-note priority, record a detailed P2 cycle, index this plan, and retain native/device verification limitations.

### Task 4: Run full portable verification

Run root and external-directory `/usr/bin/make check`, `git diff --check`, and artifact checks. Record Xcode/watch hardware as unavailable rather than claiming native execution.

## Verification Completed

- The RED contract failed because README lacked the dedicated HealthKit target
  configuration section.
- `python3 scripts/check_watchos_contracts.py` passed after adding source-backed
  entitlement, privacy, version, signing, and provisioning guidance.
- Root and external-directory `/usr/bin/make check` passed; Xcode and physical
  Apple Watch execution were unavailable and remain covered by the documented
  device checklist.
