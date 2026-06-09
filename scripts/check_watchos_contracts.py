#!/usr/bin/env python3
"""Static privacy and project contract checks for the legacy WatchKit sample."""
import plistlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-healthkit-privacy-strings.md"
INTERFACE_CONTROLLER = ROOT / "HeartyMonitor WatchKit Extension" / "InterfaceController.swift"

HEALTHKIT_INFO_PLISTS = [
    Path("HeartyMonitor/Info.plist"),
    Path("HeartyMonitor WatchKit Extension/Info.plist"),
    Path("HeartyMonitorUITests/HeartyMonitor/Info.plist"),
    Path("HeartyMonitorUITests/HeartyMonitor WatchKit Extension/Info.plist"),
]

HEALTHKIT_ENTITLEMENTS = [
    Path("HeartyMonitor/HeartyMonitor.entitlements"),
    Path("HeartyMonitor WatchKit Extension/HeartyMonitor WatchKit Extension.entitlements"),
    Path("HeartyMonitorUITests/HeartyMonitor/HeartyMonitor.entitlements"),
    Path("HeartyMonitorUITests/HeartyMonitor WatchKit Extension/HeartyMonitor WatchKit Extension.entitlements"),
]

EXPECTED_SHARE_DESCRIPTION = (
    "HeartyMonitor reads heart-rate data to display live workout feedback on the watch."
)


def read_plist(relative_path):
    path = ROOT / relative_path
    with path.open("rb") as plist_file:
        return plistlib.load(plist_file)


def assert_true(condition, label):
    if not condition:
        raise AssertionError(label)


def test_healthkit_plists_have_share_usage_description():
    for relative_path in HEALTHKIT_INFO_PLISTS:
        plist = read_plist(relative_path)
        description = plist.get("NSHealthShareUsageDescription")
        assert_true(
            description == EXPECTED_SHARE_DESCRIPTION,
            "{0} must declare NSHealthShareUsageDescription".format(relative_path),
        )


def test_healthkit_entitlements_are_enabled():
    for relative_path in HEALTHKIT_ENTITLEMENTS:
        entitlements = read_plist(relative_path)
        assert_true(
            entitlements.get("com.apple.developer.healthkit") is True,
            "{0} must keep the HealthKit entitlement enabled".format(relative_path),
        )


def test_completed_plan_is_in_docs_plans():
    assert_true(PLAN_PATH.is_file(), "HealthKit privacy plan must live under docs/plans")
    plan_text = PLAN_PATH.read_text()
    assert_true(
        "status: completed" in plan_text.lower(),
        "HealthKit privacy plan must be marked completed",
    )
    assert_true("make check" in plan_text, "HealthKit privacy plan must document make check verification")


def test_heart_rate_streaming_query_is_retained_and_stopped():
    source = INTERFACE_CONTROLLER.read_text()
    assert_true(
        "var heartRateQuery" in source,
        "InterfaceController must retain the active heart-rate query",
    )
    assert_true(
        "heartRateQuery = query" in source or "self.heartRateQuery = query" in source,
        "workoutDidStart must store the query it executes",
    )
    assert_true(
        "if let query = heartRateQuery" in source or "if let query = self.heartRateQuery" in source,
        "workoutDidEnd must stop the retained query",
    )
    assert_true(
        "heartRateQuery = nil" in source or "self.heartRateQuery = nil" in source,
        "workoutDidEnd must clear the retained query after stopping it",
    )


def test_healthkit_update_handler_guards_anchor():
    source = INTERFACE_CONTROLLER.read_text()
    assert_true(
        "newAnchor!" not in source,
        "HealthKit update handlers must not force-unwrap newAnchor",
    )
    assert_true(
        "guard let newAnchor = newAnchor else" in source,
        "HealthKit update handlers must ignore callbacks without a new anchor",
    )


def main():
    tests = [
        test_healthkit_plists_have_share_usage_description,
        test_healthkit_entitlements_are_enabled,
        test_completed_plan_is_in_docs_plans,
        test_heart_rate_streaming_query_is_retained_and_stopped,
        test_healthkit_update_handler_guards_anchor,
    ]
    for test in tests:
        test()
    print("watchos contract checks passed ({0} tests)".format(len(tests)))


if __name__ == "__main__":
    main()
