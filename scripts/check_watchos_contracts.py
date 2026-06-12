#!/usr/bin/env python3
"""Static privacy and project contract checks for the legacy WatchKit sample."""
import plistlib
from pathlib import Path

from workflow_contract import validate as validate_workflow


ROOT = Path(__file__).resolve().parents[1]
HEALTHKIT_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-healthkit-privacy-strings.md"
UITEST_MIRROR_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-watchkit-uitest-query-mirror.md"
SESSION_START_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-08-watchkit-session-start.md"
SESSION_FAILURE_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-watchkit-session-failure-ui.md"
SESSION_END_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-09-watchkit-session-end-ui.md"
AUTHORIZATION_MAIN_THREAD_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-09-watchkit-authorization-main-thread.md"
)
AUTHORIZATION_START_BUTTON_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-09-watchkit-authorization-start-button.md"
)
QUERY_FAILURE_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-09-watchkit-query-start-failure-ui.md"
)
HEART_RATE_VALUE_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-09-watchkit-heart-rate-value-bounds.md"
)
SESSION_DELEGATE_MAIN_THREAD_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-09-watchkit-session-delegate-main-thread.md"
)
HEART_RATE_INACTIVE_CALLBACK_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-09-watchkit-inactive-heart-rate-callbacks.md"
)
CI_PLAN_PATH = ROOT / "docs" / "plans" / "2026-06-10-ci-baseline.md"
MAIN_QUEUE_STALE_CALLBACK_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-10-main-queue-stale-heart-rate-callback.md"
)
LATEST_SAMPLE_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-10-latest-heart-rate-sample.md"
)
AUTHORIZATION_LIFECYCLE_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-12-authorization-lifecycle-guard.md"
)
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "check.yml"
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
    assert_completed_plan(AUTHORIZATION_MAIN_THREAD_PLAN_PATH, "WatchKit authorization main thread")
    assert_completed_plan(AUTHORIZATION_START_BUTTON_PLAN_PATH, "WatchKit authorization start button")
    assert_completed_plan(QUERY_FAILURE_PLAN_PATH, "WatchKit query start failure UI")
    assert_completed_plan(HEART_RATE_VALUE_PLAN_PATH, "WatchKit heart-rate value bounds")
    assert_completed_plan(SESSION_DELEGATE_MAIN_THREAD_PLAN_PATH, "WatchKit session delegate main thread")
    assert_completed_plan(HEART_RATE_INACTIVE_CALLBACK_PLAN_PATH, "WatchKit inactive heart-rate callbacks")
    assert_completed_plan(CI_PLAN_PATH, "GitHub Actions CI baseline")
    assert_completed_plan(MAIN_QUEUE_STALE_CALLBACK_PLAN_PATH, "main-queue stale heart-rate callback")
    assert_completed_plan(LATEST_SAMPLE_PLAN_PATH, "latest heart-rate sample")
    assert_completed_plan(AUTHORIZATION_LIFECYCLE_PLAN_PATH, "authorization lifecycle guard")


def test_ci_workflow_runs_static_baseline():
    assert_true(WORKFLOW_PATH.is_file(), "GitHub Actions check workflow must exist")
    workflow = WORKFLOW_PATH.read_text()
    errors = validate_workflow(workflow)
    assert_true(not errors, "CI workflow must {0}".format(errors[0]) if errors else "")

    makefile = (ROOT / "Makefile").read_text()
    assert_true("ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))" in makefile, "Makefile must resolve the repository root")
    assert_true("PROJECT := $(ROOT)/HeartyMonitor.xcodeproj" in makefile, "Makefile must use the rooted project path")
    assert_true("$(ROOT)/scripts/check_watchos_contracts.py" in makefile, "Makefile must use the rooted contract path")
    assert_true("WORKFLOW_CONTRACT_SCRIPT" in makefile, "Makefile must define the workflow mutation checker")
    assert_true('find "$(ROOT)"' in makefile, "Makefile cleanup must stay inside the repository")
    assert_true(
        '$(MAKE) -f "$(abspath $(lastword $(MAKEFILE_LIST)))" clean' in makefile,
        "Makefile final cleanup must remain root-independent",
    )

    for relative_path in ["README.md", "VISION.md", "SECURITY.md", "CHANGES.md"]:
        doc = (ROOT / relative_path).read_text()
        assert_true(
            "GitHub Actions" in doc,
            "{0} must document the hosted static baseline".format(relative_path),
        )


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


def test_authorization_denial_updates_ui_on_main_queue():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        authorization_block = source.split(
            "healthStore.requestAuthorizationToShareTypes", 1
        )[1].split("func displayNotAllowed", 1)[0]
        assert_true(
            "if success == false" in authorization_block,
            "{0} must handle denied HealthKit authorization".format(relative_path),
        )
        assert_true(
            "dispatch_async(dispatch_get_main_queue())" in authorization_block,
            "{0} must dispatch denied-authorization UI updates to the main queue".format(relative_path),
        )
        assert_true(
            "self.displayNotAllowed()" in authorization_block,
            "{0} must still show denied-authorization feedback".format(relative_path),
        )
        assert_true(
            authorization_block.index("dispatch_async(dispatch_get_main_queue())")
            < authorization_block.index("self.displayNotAllowed()"),
            "{0} must dispatch before updating denied-authorization UI".format(relative_path),
        )


def test_healthkit_authorization_controls_start_button_state():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        will_activate = source.split("override func willActivate()", 1)[1].split(
            "func displayNotAllowed", 1
        )[0]
        unavailable_block = will_activate.split(
            "guard HKHealthStore.isHealthDataAvailable() == true else", 1
        )[1].split("guard let quantityType", 1)[0]
        authorization_setup = will_activate.split(
            "let dataTypes = Set(arrayLiteral: quantityType)", 1
        )[1]
        authorization_block = source.split(
            "healthStore.requestAuthorizationToShareTypes", 1
        )[1].split("func displayNotAllowed", 1)[0]
        display_not_allowed = source.split("func displayNotAllowed()", 1)[1].split(
            "func workoutSession", 1
        )[0]

        assert_true(
            "startStopButton.setEnabled(false)" in unavailable_block,
            "{0} must disable Start when HealthKit data is unavailable".format(relative_path),
        )
        assert_true(
            "startStopButton.setEnabled(false)" in display_not_allowed,
            "{0} denied HealthKit feedback must disable Start".format(relative_path),
        )
        assert_true(
            authorization_setup.index("startStopButton.setEnabled(false)")
            < authorization_setup.index("healthStore.requestAuthorizationToShareTypes"),
            "{0} must disable Start while HealthKit authorization is pending".format(relative_path),
        )
        assert_true(
            "if success == true" in authorization_block,
            "{0} must explicitly handle successful HealthKit authorization".format(relative_path),
        )
        assert_true(
            "self.startStopButton.setEnabled(true)" in authorization_block,
            "{0} must re-enable Start after successful HealthKit authorization".format(relative_path),
        )
        assert_true(
            authorization_block.index("dispatch_async(dispatch_get_main_queue())")
            < authorization_block.index("self.startStopButton.setEnabled(true)"),
            "{0} must re-enable Start on the main queue".format(relative_path),
        )


def test_authorization_callbacks_ignore_inactive_interfaces():
    sources = []
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        sources.append(source)
        will_activate = source.split("override func willActivate()", 1)[1].split(
            "override func didDeactivate()", 1
        )[0]
        authorization_block = will_activate.split(
            "healthStore.requestAuthorizationToShareTypes", 1
        )[1]
        did_deactivate = source.split("override func didDeactivate()", 1)[1].split(
            "func displayNotAllowed", 1
        )[0]

        assert_true(
            "var interfaceActive = false" in source,
            "{0} must track interface lifecycle state".format(relative_path),
        )
        assert_true(
            will_activate.index("interfaceActive = true")
            < will_activate.index("healthStore.requestAuthorizationToShareTypes"),
            "{0} must mark activation before requesting authorization".format(relative_path),
        )
        assert_true(
            "guard self.interfaceActive else { return }" in authorization_block,
            "{0} must ignore stale authorization UI work".format(relative_path),
        )
        assert_true(
            authorization_block.index("dispatch_async(dispatch_get_main_queue())")
            < authorization_block.index("guard self.interfaceActive else { return }")
            < authorization_block.index("if success == true"),
            "{0} must recheck lifecycle state on the main queue before UI updates".format(relative_path),
        )
        assert_true(
            did_deactivate.index("interfaceActive = false")
            < did_deactivate.index("super.didDeactivate()"),
            "{0} must invalidate callbacks during deactivation".format(relative_path),
        )

    assert_true(sources[0] == sources[1], "WatchKit source and UI-test mirror controllers must remain identical")


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


def test_heart_rate_callbacks_ignore_inactive_workouts():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        method = source.split("func createHeartRateStreamingQuery", 1)[1].split("func updateHeartRate", 1)[0]
        assert_true(
            method.count("guard self.workoutActive else {return}") >= 2,
            "{0} heart-rate callbacks must ignore inactive workouts".format(relative_path),
        )
        assert_true(
            method.index("guard self.workoutActive else {return}")
            < method.index("self.anchor = newAnchor"),
            "{0} heart-rate callbacks must check workout state before anchor/UI updates".format(relative_path),
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


def test_heart_rate_query_failure_resets_ui_state():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        method = source.split("func workoutDidStart", 1)[1].split("func workoutDidEnd", 1)[0]
        assert_true(
            'label.setText("cannot start")' in method,
            "{0} query failures must show visible failure text".format(relative_path),
        )
        assert_true(
            "workoutActive = false" in method,
            "{0} query failures must reset workoutActive".format(relative_path),
        )
        assert_true(
            'startStopButton.setTitle("Start")' in method,
            "{0} query failures must restore the Start button title".format(relative_path),
        )
        assert_true(
            "workoutSession = nil" in method,
            "{0} query failures must clear the retained workout session".format(relative_path),
        )
        assert_true(
            "healthStore.endWorkoutSession(workout)" in method,
            "{0} query failures must end the retained workout session".format(relative_path),
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


def test_workout_session_delegate_updates_ui_on_main_queue():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        state_method = source.split(
            "func workoutSession(workoutSession: HKWorkoutSession, didChangeToState", 1
        )[1].split(
            "func workoutSession(workoutSession: HKWorkoutSession, didFailWithError", 1
        )[0]
        assert_true(
            "dispatch_async(dispatch_get_main_queue())" in state_method,
            "{0} workout state changes must dispatch UI work to the main queue".format(relative_path),
        )
        assert_true(
            state_method.index("dispatch_async(dispatch_get_main_queue())")
            < state_method.index("self.workoutDidStart(date)")
            < state_method.index("self.workoutDidEnd(date)"),
            "{0} workout start/end callbacks must run inside the main-queue block".format(relative_path),
        )

        failure_method = source.split(
            "func workoutSession(workoutSession: HKWorkoutSession, didFailWithError", 1
        )[1].split("func workoutDidStart", 1)[0]
        assert_true(
            "dispatch_async(dispatch_get_main_queue())" in failure_method,
            "{0} workout failures must dispatch UI cleanup to the main queue".format(relative_path),
        )
        assert_true(
            failure_method.index("dispatch_async(dispatch_get_main_queue())")
            < failure_method.index("self.workoutActive = false")
            < failure_method.index('self.label.setText("cannot start")'),
            "{0} workout failure cleanup must run inside the main-queue block".format(relative_path),
        )
        assert_true(
            "self.workoutSession = nil" in failure_method,
            "{0} workout failures must clear the retained workout session".format(relative_path),
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


def test_heart_rate_values_are_bounded_before_display():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        method = source.split("func updateHeartRate", 1)[1].split("func updateDeviceName", 1)[0]
        assert_true(
            "guard value >= 0 && value <= 300 else{return}" in method,
            "{0} must reject out-of-range heart-rate values before display".format(relative_path),
        )
        assert_true(
            method.index("guard value >= 0 && value <= 300 else{return}")
            < method.index("String(UInt16(value))"),
            "{0} must bound heart-rate values before UInt16 display conversion".format(relative_path),
        )


def test_heart_rate_batches_display_latest_sample():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        method = source.split("func updateHeartRate", 1)[1].split("func updateDeviceName", 1)[0]
        assert_true(
            "guard let sample = heartRateSamples.last else{return}" in method,
            "{0} must display the newest sample from each callback batch".format(relative_path),
        )
        assert_true(
            "heartRateSamples.first" not in method,
            "{0} must not discard newer samples by selecting the oldest batch value".format(relative_path),
        )


def test_main_queue_heart_rate_updates_recheck_workout_state():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        method = source.split("func updateHeartRate", 1)[1].split("func updateDeviceName", 1)[0]
        assert_true(
            "dispatch_async(dispatch_get_main_queue())" in method,
            "{0} heart-rate UI updates must use the main queue".format(relative_path),
        )
        assert_true(
            "guard self.workoutActive else{return}" in method,
            "{0} must reject stale heart-rate UI work after queueing".format(relative_path),
        )
        assert_true(
            method.index("dispatch_async(dispatch_get_main_queue())")
            < method.index("guard self.workoutActive else{return}")
            < method.index("guard let sample = heartRateSamples.last else{return}"),
            "{0} must recheck workout state before reading samples on the main queue".format(relative_path),
        )


def main():
    tests = [
        test_healthkit_plists_have_share_usage_description,
        test_healthkit_entitlements_are_enabled,
        test_completed_plans_are_in_docs_plans,
        test_ci_workflow_runs_static_baseline,
        test_heart_rate_streaming_query_is_retained_and_stopped,
        test_authorization_denial_updates_ui_on_main_queue,
        test_healthkit_authorization_controls_start_button_state,
        test_authorization_callbacks_ignore_inactive_interfaces,
        test_healthkit_update_handler_guards_anchor,
        test_heart_rate_callbacks_ignore_inactive_workouts,
        test_workout_session_start_avoids_optional_force_unwrap,
        test_heart_rate_query_failure_resets_ui_state,
        test_workout_session_failure_resets_ui_without_sensitive_logs,
        test_workout_session_delegate_updates_ui_on_main_queue,
        test_workout_session_end_resets_ui_state,
        test_heart_rate_values_are_bounded_before_display,
        test_heart_rate_batches_display_latest_sample,
        test_main_queue_heart_rate_updates_recheck_workout_state,
    ]
    for test in tests:
        test()
    print("watchos contract checks passed ({0} tests)".format(len(tests)))


if __name__ == "__main__":
    main()
