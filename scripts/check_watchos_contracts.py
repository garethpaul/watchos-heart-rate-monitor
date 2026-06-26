#!/usr/bin/env python3
"""Static privacy and project contract checks for the legacy WatchKit sample."""
import plistlib
from pathlib import Path

from heart_animation_generation_contract import validation_errors as heart_animation_errors
from heart_rate_query_ownership_contract import validation_errors as query_ownership_errors
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
STALE_SESSION_CALLBACK_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-13-stale-workout-session-callbacks.md"
)
IMMEDIATE_QUERY_STOP_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-13-watchkit-immediate-query-stop.md"
)
AUTHORIZATION_GENERATION_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-13-authorization-callback-generation.md"
)
MAKE_ROOT_PROTECTION_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-14-make-root-override-protection.md"
)
DEVICE_VERIFICATION_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-14-device-verification-checklist.md"
)
CURRENT_QUERY_CALLBACK_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-16-current-heart-rate-query-callback.md"
)
QUERY_ERROR_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-16-heart-rate-query-error.md"
)
HEART_ANIMATION_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-17-heart-animation-generation.md"
)
QUERY_OWNERSHIP_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-19-watchos-main-queue-query-ownership.md"
)
MAKE_AUTHORITY_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-21-make-authority-isolation.md"
)
AUTHORIZATION_RESULT_SEMANTICS_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-25-healthkit-authorization-result-semantics.md"
)
WORKOUT_SAMPLE_ADMISSION_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-26-workout-sample-admission.md"
)
HEALTHKIT_SETUP_PLAN_PATH = (
    ROOT / "docs" / "plans" / "2026-06-26-healthkit-setup-guide.md"
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


def test_readme_documents_healthkit_target_setup():
    readme = " ".join((ROOT / "README.md").read_text().split())
    for phrase in (
        "HealthKit Target Configuration",
        "HeartyMonitor/HeartyMonitor.entitlements",
        "HeartyMonitor WatchKit Extension/HeartyMonitor WatchKit Extension.entitlements",
        "com.apple.developer.healthkit",
        "NSHealthShareUsageDescription",
        "iOS 9.2 and watchOS 2.1 deployment targets",
        "Do not commit signing identities, provisioning profiles, team identifiers, or private entitlements",
    ):
        assert_true(
            phrase in readme,
            "README HealthKit setup must preserve: {0}".format(phrase),
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
    assert_completed_plan(STALE_SESSION_CALLBACK_PLAN_PATH, "stale workout session callbacks")
    assert_completed_plan(IMMEDIATE_QUERY_STOP_PLAN_PATH, "immediate heart-rate query stop")
    assert_completed_plan(AUTHORIZATION_GENERATION_PLAN_PATH, "authorization callback generation")
    assert_completed_plan(MAKE_ROOT_PROTECTION_PLAN_PATH, "Make root override protection")
    assert_completed_plan(DEVICE_VERIFICATION_PLAN_PATH, "device verification checklist")
    assert_completed_plan(CURRENT_QUERY_CALLBACK_PLAN_PATH, "current heart-rate query callback")
    assert_completed_plan(QUERY_ERROR_PLAN_PATH, "heart-rate query error handling")
    assert_completed_plan(HEART_ANIMATION_PLAN_PATH, "heart animation generation")
    assert_completed_plan(QUERY_OWNERSHIP_PLAN_PATH, "main-queue query ownership")
    assert_completed_plan(MAKE_AUTHORITY_PLAN_PATH, "Make authority isolation")
    assert_completed_plan(
        AUTHORIZATION_RESULT_SEMANTICS_PLAN_PATH,
        "HealthKit authorization result semantics",
    )
    assert_completed_plan(WORKOUT_SAMPLE_ADMISSION_PLAN_PATH, "workout sample admission")
    assert_completed_plan(HEALTHKIT_SETUP_PLAN_PATH, "HealthKit setup guide")
    checker_main = Path(__file__).read_text().rsplit("def main():", 1)[1]
    assert_true(
        "test_device_verification_checklist_is_auditable," in checker_main,
        "device verification checklist contract must run in the main suite",
    )
    assert_true(
        "test_heart_rate_callbacks_match_current_query," in checker_main,
        "current heart-rate query callback contract must run in the main suite",
    )
    assert_true(
        "test_heart_rate_query_errors_fail_closed," in checker_main,
        "heart-rate query error contract must run in the main suite",
    )
    assert_true(
        "test_heart_animation_generation_guards," in checker_main,
        "heart animation generation contract must run in the main suite",
    )
    assert_true(
        "test_heart_rate_query_ownership_guards," in checker_main,
        "heart-rate query ownership contract must run in the main suite",
    )


def test_heart_animation_generation_guards():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        errors = heart_animation_errors(source)
        assert_true(
            not errors,
            "{0}: {1}".format(relative_path, "; ".join(errors)),
        )


def test_heart_rate_query_ownership_guards():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        errors = query_ownership_errors(source)
        assert_true(
            not errors,
            "{0}: {1}".format(relative_path, "; ".join(errors)),
        )


def test_device_verification_checklist_is_auditable():
    checklist = (ROOT / "DEVICE_VERIFICATION.md").read_text()
    normalized_checklist = " ".join(checklist.split())
    readme = (ROOT / "README.md").read_text()
    vision = (ROOT / "VISION.md").read_text()
    changes = (ROOT / "CHANGES.md").read_text()

    for phrase in (
        "Execution status: Not yet executed",
        "physical Apple Watch",
        "Do not record raw heart-rate values",
        "deny heart-rate read access",
        "callback success does not reveal the read-access decision",
        "no unauthorized heart-rate sample is displayed",
        "Do not treat an empty result as proof of denial",
        "Grant heart-rate read access",
        "button title changes from `Start` to",
        "heart-rate label updates",
        "sample source label",
        "button title returns to `Start`",
        "heart-rate label returns to `---`",
        "interrupt the workout session",
        "then relaunch",
        "watch model, watchOS version, paired iPhone iOS version, Xcode",
        "redacted pass/fail evidence",
        "Unresolved failures block merge",
    ):
        assert_true(
            phrase in normalized_checklist,
            "device verification checklist must include {0}".format(phrase),
        )
    assert_true("`DEVICE_VERIFICATION.md`" in readme, "README must link the device checklist")
    assert_true(
        "docs/plans/2026-06-14-device-verification-checklist.md" in readme,
        "README must link the device verification plan",
    )
    assert_true(
        "Require auditable physical Apple Watch verification" in vision,
        "VISION must preserve physical-device verification",
    )
    assert_true(
        "privacy-preserving physical Apple Watch verification checklist" in changes,
        "CHANGES must record the device verification checklist",
    )


def test_ci_workflow_runs_static_baseline():
    assert_true(WORKFLOW_PATH.is_file(), "GitHub Actions check workflow must exist")
    workflow = WORKFLOW_PATH.read_text()
    errors = validate_workflow(workflow)
    assert_true(not errors, "CI workflow must {0}".format(errors[0]) if errors else "")

    makefile = (ROOT / "Makefile").read_text()
    makefile_lines = set(makefile.splitlines())
    for contract in (
        ".DEFAULT_GOAL := check",
        ".SECONDEXPANSION:",
        "PYTHON ?= python3",
        "override PYTHON := $(value PYTHON)",
        "XCODEBUILD ?= /usr/bin/xcodebuild",
        "override XCODEBUILD := $(value XCODEBUILD)",
        "override SHELL := /bin/sh",
        "override .SHELLFLAGS := -c",
        "override MAKEFILES :=",
        "ifneq ($(origin MAKEFILE_LIST),file)",
        "export ROOT",
        "root-test::",
        "\t/bin/sh '$(REPOSITORY_ROOT_LITERAL)/scripts/test-makefile-root.sh'",
    ):
        assert_true(contract in makefile_lines, "Makefile authority contract is missing {0!r}".format(contract))
    assert_true("MAKEFLAGS must not be overridden" in makefile, "Makefile must reject caller MAKEFLAGS")
    assert_true("MAKEFILES must be empty" in makefile, "Makefile must reject startup files")
    assert_true("MAKEFILE_LIST must not be overridden" in makefile, "Makefile must reject Makefile-list replacement")
    assert_true("PYTHON must be a literal executable path" in makefile, "Makefile must reject Python Make syntax")
    assert_true("XCODEBUILD must be a literal executable path" in makefile, "Makefile must reject Xcode Make syntax")
    assert_true("'$(REPOSITORY_ROOT_LITERAL)/HeartyMonitor.xcodeproj'" in makefile, "Makefile must use the rooted project path")
    assert_true("'$(REPOSITORY_ROOT_LITERAL)/scripts/check_watchos_contracts.py'" in makefile, "Makefile must use the rooted contract path")
    assert_true("test_workflow_contract.py" in makefile, "Makefile must retain the workflow mutation checker")
    assert_true("/usr/bin/find '$(REPOSITORY_ROOT_LITERAL)'" in makefile, "Makefile cleanup must stay inside the repository")
    assert_true("verify:: root-test lint test contract-test build" in makefile_lines, "full verification must run authority tests")

    authority_test = (ROOT / "scripts" / "test-makefile-root.sh").read_text()
    for contract in (
        "40 target/authority cases",
        "literal hostile Python path",
        "6 raw Make-syntax controls",
        "2 MAKEFILE_LIST rejections",
        "2 startup-boundary cases",
        "8 later recipe-replacement rejections",
        "PATH-Xcode rejection",
        "cleanup containment",
        "10 mode rejections",
    ):
        assert_true(contract in authority_test, "Make authority harness must include {0!r}".format(contract))

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


def test_authorization_request_errors_update_ui_on_main_queue():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        authorization_block = source.split(
            "healthStore.requestAuthorizationToShareTypes", 1
        )[1].split("func displayAuthorizationFailed", 1)[0]
        assert_true(
            "if success == false" in authorization_block,
            "{0} must handle HealthKit authorization request errors".format(relative_path),
        )
        assert_true(
            "dispatch_async(dispatch_get_main_queue())" in authorization_block,
            "{0} must dispatch authorization-error UI updates to the main queue".format(relative_path),
        )
        assert_true(
            "self.displayAuthorizationFailed()" in authorization_block,
            "{0} must show authorization request failure feedback".format(relative_path),
        )
        assert_true(
            authorization_block.index("dispatch_async(dispatch_get_main_queue())")
            < authorization_block.index("self.displayAuthorizationFailed()"),
            "{0} must dispatch before updating authorization-error UI".format(relative_path),
        )
        assert_true(
            'updateStatusText("authorization failed")' in source,
            "{0} must distinguish request processing errors from unobservable read denial".format(relative_path),
        )
        assert_true(
            '"not allowed"' not in source,
            "{0} must not claim HealthKit read denial is observable".format(relative_path),
        )


def test_healthkit_authorization_controls_start_button_state():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        will_activate = source.split("override func willActivate()", 1)[1].split(
            "func displayAuthorizationFailed", 1
        )[0]
        unavailable_block = will_activate.split(
            "guard HKHealthStore.isHealthDataAvailable() == true else", 1
        )[1].split("guard let quantityType", 1)[0]
        authorization_setup = will_activate.split(
            "let dataTypes = Set(arrayLiteral: quantityType)", 1
        )[1]
        authorization_block = source.split(
            "healthStore.requestAuthorizationToShareTypes", 1
        )[1].split("func displayAuthorizationFailed", 1)[0]
        display_authorization_failed = source.split("func displayAuthorizationFailed()", 1)[1].split(
            "func workoutSession", 1
        )[0]

        assert_true(
            "startStopButton.setEnabled(false)" in unavailable_block,
            "{0} must disable Start when HealthKit data is unavailable".format(relative_path),
        )
        assert_true(
            "startStopButton.setEnabled(false)" in display_authorization_failed,
            "{0} authorization error feedback must disable Start".format(relative_path),
        )
        assert_true(
            authorization_setup.index("startStopButton.setEnabled(false)")
            < authorization_setup.index("healthStore.requestAuthorizationToShareTypes"),
            "{0} must disable Start while HealthKit authorization is pending".format(relative_path),
        )
        assert_true(
            "if success == true" in authorization_block,
            "{0} must explicitly handle successful HealthKit authorization request processing".format(relative_path),
        )
        assert_true(
            "self.startStopButton.setEnabled(true)" in authorization_block,
            "{0} must re-enable Start after successful HealthKit authorization request processing".format(relative_path),
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
            "func displayAuthorizationFailed", 1
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
            "guard self.interfaceActive" in authorization_block,
            "{0} must ignore stale authorization UI work".format(relative_path),
        )
        assert_true(
            authorization_block.index("dispatch_async(dispatch_get_main_queue())")
            < authorization_block.index("guard self.interfaceActive")
            < authorization_block.index("if success == true"),
            "{0} must recheck lifecycle state on the main queue before UI updates".format(relative_path),
        )
        assert_true(
            did_deactivate.index("interfaceActive = false")
            < did_deactivate.index("super.didDeactivate()"),
            "{0} must invalidate callbacks during deactivation".format(relative_path),
        )

    assert_true(sources[0] == sources[1], "WatchKit source and UI-test mirror controllers must remain identical")


def test_authorization_callbacks_match_current_activation_generation():
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
            "func displayAuthorizationFailed", 1
        )[0]

        assert_true(
            "var authorizationGeneration = 0" in source,
            "{0} must track authorization activation generations".format(relative_path),
        )
        assert_true(
            will_activate.index("interfaceActive = true")
            < will_activate.index("authorizationGeneration += 1")
            < will_activate.index("let activationGeneration = authorizationGeneration")
            < will_activate.index("healthStore.requestAuthorizationToShareTypes"),
            "{0} must advance and capture the generation before authorization".format(relative_path),
        )
        assert_true(
            "self.authorizationGeneration == activationGeneration" in authorization_block,
            "{0} must reject callbacks from older activations".format(relative_path),
        )
        assert_true(
            authorization_block.index("dispatch_async(dispatch_get_main_queue())")
            < authorization_block.index("self.authorizationGeneration == activationGeneration")
            < authorization_block.index("if success == true"),
            "{0} must compare generations on the main queue before UI updates".format(relative_path),
        )
        assert_true(
            did_deactivate.index("interfaceActive = false")
            < did_deactivate.index("authorizationGeneration += 1")
            < did_deactivate.index("super.didDeactivate()"),
            "{0} must invalidate the authorization generation during deactivation".format(relative_path),
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
        method = source.split("func handleHeartRateQueryResult", 1)[1].split(
            "func heartRateQueryDidFail", 1
        )[0]
        assert_true(
            "guard workoutActive else {return}" in method,
            "{0} heart-rate callbacks must ignore inactive workouts".format(relative_path),
        )
        assert_true(
            method.index("guard workoutActive else {return}")
            < method.index("anchor = newAnchor"),
            "{0} heart-rate callbacks must check workout state before anchor/UI updates".format(relative_path),
        )


def test_heart_rate_callbacks_match_current_query():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        query_factory = source.split("func createHeartRateStreamingQuery", 1)[1].split(
            "func handleHeartRateQueryResult", 1
        )[0]
        initial_callback, update_callback = query_factory.split("heartRateQuery.updateHandler", 1)
        for callback_name, callback in (
            ("initial", initial_callback),
            ("update", update_callback),
        ):
            assert_true(
                "dispatch_async(dispatch_get_main_queue())" in callback
                and "self.handleHeartRateQueryResult(" in callback,
                "{0} {1} callback must route through main-queue ownership".format(
                    relative_path, callback_name
                ),
            )

        owner = source.split("func handleHeartRateQueryResult", 1)[1].split(
            "func heartRateQueryDidFail", 1
        )[0]
        query_guard = "guard heartRateQuery === query else {return}"
        assert_true(
            owner.index(query_guard)
            < owner.index("anchor = newAnchor")
            < owner.index("updateHeartRate(samples, query: query)"),
            "{0} main-queue owner must match the retained query before anchor mutation".format(
                relative_path
            ),
        )

        update_method = source.split("func updateHeartRate", 1)[1].split(
            "func updateStatusText", 1
        )[0]
        queued_query_guard = "guard self.heartRateQuery === query else{return}"
        assert_true(
            "(samples: [HKSample]?, query: HKQuery)" in update_method,
            "{0} heart-rate UI work must retain callback query identity".format(
                relative_path
            ),
        )
        assert_true(
            queued_query_guard in update_method,
            "{0} heart-rate UI work must reject stale queries".format(relative_path),
        )
        assert_true(
            "dispatch_async(" not in update_method
            and update_method.index(queued_query_guard)
            < update_method.index("guard let sample = heartRateSamples.last else{return}"),
            "{0} main-queue UI work must match the retained query before reading samples".format(
                relative_path
            ),
        )


def test_heart_rate_query_errors_fail_closed():
    sources = []
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        sources.append(source)
        query_method = source.split("func createHeartRateStreamingQuery", 1)[1].split(
            "func handleHeartRateQueryResult", 1
        )[0]
        initial_callback, update_callback = query_method.split("heartRateQuery.updateHandler", 1)
        for callback_name, callback in (
            ("initial", initial_callback),
            ("update", update_callback),
        ):
            for contract in (
                "dispatch_async(dispatch_get_main_queue())",
                "self.handleHeartRateQueryResult(",
            ):
                assert_true(
                    contract in callback,
                    "{0} {1} callback must include {2}".format(
                        relative_path, callback_name, contract
                    ),
                )

        owner = source.split("func handleHeartRateQueryResult", 1)[1].split(
            "func heartRateQueryDidFail", 1
        )[0]
        owner_contracts = (
            "guard workoutActive else {return}",
            "guard heartRateQuery === query else {return}",
            "guard error == nil else",
            "heartRateQueryDidFail(query)",
            "guard let newAnchor = newAnchor else {return}",
            "anchor = newAnchor",
        )
        owner_positions = [owner.index(contract) for contract in owner_contracts]
        assert_true(
            owner_positions == sorted(owner_positions),
            "{0} query owner must reject current-query errors before anchor processing".format(
                relative_path
            ),
        )

        failure_method = source.split("func heartRateQueryDidFail", 1)[1].split(
            "func updateHeartRate", 1
        )[0]
        ordered_contracts = (
            "guard self.workoutActive else {return}",
            "guard self.heartRateQuery === query else {return}",
            "self.workoutActive = false",
            'self.startStopButton.setTitle("Start")',
            "self.healthStore.stopQuery(query)",
            "self.heartRateQuery = nil",
            "self.workoutSession = nil",
            "self.healthStore.endWorkoutSession(workout)",
            'self.updateDeviceName("")',
            'self.updateStatusText("cannot start")',
            'NSLog("Heart-rate query failed")',
        )
        positions = [failure_method.index(contract) for contract in ordered_contracts]
        assert_true(
            positions == sorted(positions),
            "{0} query failure must validate identity and clear query/session UI state in order".format(
                relative_path
            ),
        )
        assert_true(
            "NSLog(error" not in failure_method and "localizedDescription" not in source,
            "{0} query failure logs must not expose HealthKit error details".format(relative_path),
        )

    assert_true(
        sources[0] == sources[1],
        "WatchKit source and UI-test mirror controllers must remain identical",
    )

    docs = {
        "README.md": "Heart-rate query errors stop and clear the current query and workout",
        "SECURITY.md": "Heart-rate query errors fail closed without logging HealthKit details",
        "VISION.md": "Fail closed when the current heart-rate query reports an error",
        "CHANGES.md": "Failed closed when the current heart-rate streaming query reports an error",
    }
    for relative_path, phrase in docs.items():
        assert_true(
            phrase in (ROOT / relative_path).read_text(),
            "{0} must document heart-rate query error handling".format(relative_path),
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


def test_stopping_workout_immediately_stops_heart_rate_query():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        action = source.split("@IBAction func startBtnTapped()", 1)[1].split(
            "func startWorkout()", 1
        )[0]
        stop_branch = action.split("} else {", 1)[0]
        query_guard = "if let query = self.heartRateQuery"
        stop_query = "self.healthStore.stopQuery(query)"
        clear_query = "self.heartRateQuery = nil"
        clear_session = "self.workoutSession = nil"
        end_session = "healthStore.endWorkoutSession(workout)"

        for contract in (query_guard, stop_query, clear_query, clear_session, end_session):
            assert_true(
                contract in stop_branch,
                "{0} Stop branch must keep {1}".format(relative_path, contract),
            )
        assert_true(
            stop_branch.index(query_guard)
            < stop_branch.index(stop_query)
            < stop_branch.index(clear_query)
            < stop_branch.index(clear_session)
            < stop_branch.index(end_session),
            "{0} must relinquish query and session ownership before ending the workout session".format(
                relative_path
            ),
        )


def test_heart_rate_query_failure_resets_ui_state():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        method = source.split("func workoutDidStart", 1)[1].split("func workoutDidEnd", 1)[0]
        assert_true(
            'updateStatusText("cannot start")' in method,
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
            'updateStatusText("cannot start")' in source,
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
            < state_method.index("guard self.workoutSession === workoutSession else { return }")
            < state_method.index("switch toState")
            < state_method.index("guard self.workoutActive else { return }")
            < state_method.index("self.workoutDidStart(date)")
            < state_method.index("self.workoutDidEnd(date)"),
            "{0} workout callbacks must reject stale sessions and late starts on the main queue".format(relative_path),
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
            < failure_method.index("guard self.workoutSession === workoutSession else { return }")
            < failure_method.index("self.workoutActive = false")
            < failure_method.index('self.updateStatusText("cannot start")'),
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
        method = source.split("func updateHeartRate", 1)[1].split("func updateStatusText", 1)[0]
        assert_true(
            "guard value > 0 && value <= 300 else{return}" in method,
            "{0} must reject out-of-range heart-rate values before display".format(relative_path),
        )
        assert_true(
            method.index("guard value > 0 && value <= 300 else{return}")
            < method.index("String(UInt16(value))"),
            "{0} must bound heart-rate values before UInt16 display conversion".format(relative_path),
        )


def test_heart_rate_batches_display_latest_sample():
    for relative_path in INTERFACE_CONTROLLERS:
        source = (ROOT / relative_path).read_text()
        method = source.split("func updateHeartRate", 1)[1].split("func updateStatusText", 1)[0]
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
        factory = source.split("func createHeartRateStreamingQuery", 1)[1].split(
            "func handleHeartRateQueryResult", 1
        )[0]
        owner = source.split("func handleHeartRateQueryResult", 1)[1].split(
            "func heartRateQueryDidFail", 1
        )[0]
        method = source.split("func updateHeartRate", 1)[1].split("func updateStatusText", 1)[0]
        assert_true(
            factory.count("dispatch_async(dispatch_get_main_queue())") == 2,
            "{0} HealthKit callbacks must enter the main queue".format(relative_path),
        )
        assert_true(
            "guard self.workoutActive else{return}" in method,
            "{0} must reject stale heart-rate UI work on the main queue".format(relative_path),
        )
        assert_true(
            owner.index("guard workoutActive else {return}")
            < owner.index("guard heartRateQuery === query else {return}")
            < owner.index("anchor = newAnchor")
            and method.index("guard self.workoutActive else{return}")
            < method.index("guard let sample = heartRateSamples.last else{return}"),
            "{0} must validate state before anchor and sample processing on the main queue".format(relative_path),
        )


def main():
    tests = [
        test_healthkit_plists_have_share_usage_description,
        test_healthkit_entitlements_are_enabled,
        test_readme_documents_healthkit_target_setup,
        test_completed_plans_are_in_docs_plans,
        test_device_verification_checklist_is_auditable,
        test_ci_workflow_runs_static_baseline,
        test_heart_rate_streaming_query_is_retained_and_stopped,
        test_authorization_request_errors_update_ui_on_main_queue,
        test_healthkit_authorization_controls_start_button_state,
        test_authorization_callbacks_ignore_inactive_interfaces,
        test_authorization_callbacks_match_current_activation_generation,
        test_healthkit_update_handler_guards_anchor,
        test_heart_rate_callbacks_ignore_inactive_workouts,
        test_heart_rate_callbacks_match_current_query,
        test_heart_rate_query_errors_fail_closed,
        test_heart_animation_generation_guards,
        test_heart_rate_query_ownership_guards,
        test_workout_session_start_avoids_optional_force_unwrap,
        test_stopping_workout_immediately_stops_heart_rate_query,
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
