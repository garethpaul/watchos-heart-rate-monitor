#!/usr/bin/env python3
"""Static privacy and project contract checks for the legacy WatchKit sample."""
import plistlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HEALTHKIT_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-healthkit-privacy-strings.md"
UITEST_MIRROR_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-watchkit-uitest-query-mirror.md"
SESSION_START_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-watchkit-session-start.md"
SESSION_FAILURE_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-watchkit-session-failure-ui.md"
SESSION_END_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-watchkit-session-end-ui.md"
INTERFACE_CONTROLLERS = [
    Path("HeartyMonitor WatchKit Extension/InterfaceController.swift"),
    Path("HeartyMonitorUITests/HeartyMonitor WatchKit Extension/InterfaceController.swift"),
]

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


def assert_completed_plan(path, label):
    assert_true(path.is_file(), "{0} plan must live under docs/plans".format(label))
    plan_text = path.read_text()
    assert_true(
        "status: completed" in plan_text.lower(),
        "{0} plan must be marked completed".format(label),
    )
    assert_true("make check" in plan_text, "{0} plan must document make check verification".format(label))


def test_completed_plans_are_in_docs_plans():
    assert_completed_plan(HEALTHKIT_PLAN_PATH, "HealthKit privacy")
    assert_completed_plan(UITEST_MIRROR_PLAN_PATH, "UITest WatchKit mirror")
    assert_completed_plan(SESSION_START_PLAN_PATH, "WatchKit session start")
    assert_completed_plan(SESSION_FAILURE_PLAN_PATH, "WatchKit session failure UI")
    assert_completed_plan(SESSION_END_PLAN_PATH, "WatchKit session end UI")


def test_heart_rate_streaming_query_is_retained_and_stopped():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        assert_true(
            "var heartRateQuery" in source,
            "{0} must retain the active heart-rate query".format(relative_path),
        )
        assert_true(
            "heartRateQuery = query" in source or "self.heartRateQuery = query" in source,
            "{0} workoutDidStart must store the query it executes".format(relative_path),
        )
        assert_true(
            "if let query = heartRateQuery" in source or "if let query = self.heartRateQuery" in source,
            "{0} workoutDidEnd must stop the retained query".format(relative_path),
        )
        assert_true(
            "heartRateQuery = nil" in source or "self.heartRateQuery = nil" in source,
            "{0} workoutDidEnd must clear the retained query after stopping it".format(relative_path),
        )


def test_healthkit_update_handler_guards_anchor():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        assert_true(
            "newAnchor!" not in source,
            "{0} update handlers must not force-unwrap newAnchor".format(relative_path),
        )
        assert_true(
            "guard let newAnchor = newAnchor else" in source,
            "{0} update handlers must ignore callbacks without a new anchor".format(relative_path),
        )


def test_workout_session_start_avoids_optional_force_unwrap():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        assert_true(
            "startWorkoutSession(self.workoutSession!)" not in source,
            "{0} must not force-unwrap workoutSession when starting".format(relative_path),
        )
        assert_true(
            "let session = HKWorkoutSession" in source,
            "{0} must keep a local workout session before storing it".format(relative_path),
        )
        assert_true(
            "healthStore.startWorkoutSession(session)" in source,
            "{0} must start the local workout session value".format(relative_path),
        )


def test_workout_session_failure_resets_ui_without_sensitive_logs():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        assert_true(
            "error.userInfo" not in source,
            "{0} workout failures must not log error.userInfo".format(relative_path),
        )
        assert_true(
            "workoutActive = false" in source,
            "{0} workout failures must reset workoutActive".format(relative_path),
        )
        assert_true(
            'startStopButton.setTitle("Start")' in source,
            "{0} workout failures must restore the Start button title".format(relative_path),
        )
        assert_true(
            'label.setText("cannot start")' in source,
            "{0} workout failures must show visible failure text".format(relative_path),
        )
        assert_true(
            'NSLog("Workout session failed")' in source,
            "{0} workout failures must log a non-sensitive failure message".format(relative_path),
        )


def test_workout_session_end_resets_ui_state():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        method = source.split("func workoutDidEnd", 1)[1].split("// MARK", 1)[0]
        assert_true(
            "workoutActive = false" in method,
            "{0} workoutDidEnd must reset workoutActive".format(relative_path),
        )
        assert_true(
            'startStopButton.setTitle("Start")' in method,
            "{0} workoutDidEnd must restore the Start button title".format(relative_path),
        )
        assert_true(
            "workoutSession = nil" in method,
            "{0} workoutDidEnd must clear the retained workout session".format(relative_path),
        )


def main():
    tests = [
        test_healthkit_plists_have_share_usage_description,
        test_healthkit_entitlements_are_enabled,
        test_completed_plans_are_in_docs_plans,
        test_heart_rate_streaming_query_is_retained_and_stopped,
        test_healthkit_update_handler_guards_anchor,
        test_workout_session_start_avoids_optional_force_unwrap,
        test_workout_session_failure_resets_ui_without_sensitive_logs,
        test_workout_session_end_resets_ui_state,
    ]
    for test in tests:
        test()
    print("watchos contract checks passed ({0} tests)".format(len(tests)))


if __name__ == "__main__":
    main()
