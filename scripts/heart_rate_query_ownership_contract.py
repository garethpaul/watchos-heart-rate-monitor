#!/usr/bin/env python3
"""Static contract for main-queue-owned HealthKit query state."""


def function_body(source, start_marker, end_marker):
    start = source.find(start_marker)
    end = source.find(end_marker, start)
    if start < 0 or end < 0:
        return None
    return source[start:end]


def ordered(body, fragments):
    positions = [body.find(fragment) for fragment in fragments]
    return all(position >= 0 for position in positions) and positions == sorted(positions)


def validation_errors(source):
    errors = []
    query_factory = function_body(
        source,
        "func createHeartRateStreamingQuery",
        "func handleHeartRateQueryResult",
    )
    if query_factory is None:
        errors.append("query factory and result owner must remain separate")
    else:
        if not ordered(
            query_factory,
            (
                "let predicate = HKQuery.predicateForSamplesWithStartDate(",
                "options: HKQueryOptions.StrictStartDate)",
                "predicate: predicate",
            ),
        ):
            errors.append("heart-rate queries must admit only samples from the current workout")
        callback_dispatches = query_factory.count(
            "dispatch_async(dispatch_get_main_queue())"
        )
        callback_routes = query_factory.count("self.handleHeartRateQueryResult(")
        if callback_dispatches != 2 or callback_routes != 2:
            errors.append("both HealthKit callbacks must route results to the main queue")
        initial_callback, separator, update_callback = query_factory.partition(
            "heartRateQuery.updateHandler"
        )
        if not separator or not ordered(
            initial_callback,
            (
                "dispatch_async(dispatch_get_main_queue())",
                "self.handleHeartRateQueryResult(",
            ),
        ) or not ordered(
            update_callback,
            (
                "dispatch_async(dispatch_get_main_queue())",
                "self.handleHeartRateQueryResult(",
            ),
        ):
            errors.append("HealthKit callbacks must dispatch before touching controller state")

    owner = function_body(
        source,
        "func handleHeartRateQueryResult",
        "func heartRateQueryDidFail",
    )
    if owner is None or not ordered(
        owner,
        (
            "guard workoutActive else {return}",
            "guard heartRateQuery === query else {return}",
            "guard error == nil else",
            "guard let newAnchor = newAnchor else {return}",
            "anchor = newAnchor",
            "updateHeartRate(samples, query: query)",
        ),
    ):
        errors.append("main-queue result owner must validate identity before advancing anchor")
    elif "dispatch_async(" in owner:
        errors.append("result owner must execute synchronously on the main queue")

    failure = function_body(source, "func heartRateQueryDidFail", "func updateHeartRate")
    if failure is None or "dispatch_async(" in failure:
        errors.append("query failure teardown must remain main-queue synchronous")

    update = function_body(source, "func updateHeartRate", "func updateStatusText")
    if update is None or not ordered(
        update,
        (
            "guard self.workoutActive else{return}",
            "guard self.heartRateQuery === query else{return}",
            "guard let sample = heartRateSamples.last else{return}",
            "guard value > 0 && value <= 300 else{return}",
            "self.updateStatusText(String(UInt16(value)))",
            "self.updateDeviceName(name)",
        ),
    ):
        errors.append("heart-rate samples must update retained interface state on the main queue")
    elif "dispatch_async(" in update:
        errors.append("heart-rate UI updates must not introduce a second queue hop")

    status = function_body(source, "func updateStatusText", "func updateDeviceName")
    if status is None or not ordered(
        status,
        (
            "statusText = text",
            "guard interfaceActive else {return}",
            "label.setText(text)",
        ),
    ):
        errors.append("status updates must persist before touching active WatchKit UI")

    device = function_body(source, "func updateDeviceName", "func renderInterfaceState")
    if device is None or not ordered(
        device,
        (
            "currentDeviceName = deviceName",
            "guard interfaceActive else {return}",
            "deviceLabel.setText(deviceName)",
        ),
    ):
        errors.append("device updates must persist before touching active WatchKit UI")

    activation = function_body(source, "override func willActivate()", "override func didDeactivate()")
    if activation is None or not ordered(
        activation,
        (
            "interfaceActive = true",
            "resetHeartAnimation()",
            "renderInterfaceState()",
            "healthStore.requestAuthorizationToShareTypes",
        ),
    ):
        errors.append("activation must restore retained UI and reset stale animation geometry")

    stop_action = function_body(source, "@IBAction func startBtnTapped()", "func startWorkout()")
    if stop_action is None:
        errors.append("start/stop actions must clear stale UI and relinquish ending sessions")
    else:
        stop_branch, separator, start_branch = stop_action.partition("} else {")
        stop_valid = ordered(
            stop_branch,
            (
                "self.workoutActive = false",
                "self.updateStatusText(\"---\")",
                "self.updateDeviceName(\"\")",
                "if let workout = self.workoutSession",
                "self.workoutSession = nil",
                "healthStore.endWorkoutSession(workout)",
            ),
        )
        start_valid = ordered(
            start_branch,
            (
                "self.workoutActive = true",
                "self.updateStatusText(\"---\")",
                "self.updateDeviceName(\"\")",
                "startWorkout()",
            ),
        )
        if not separator or not stop_valid or not start_valid:
            errors.append("start/stop actions must clear stale UI and relinquish ending sessions")

    start_failure = function_body(source, "func workoutDidStart", "func workoutDidEnd")
    if start_failure is None or not ordered(
        start_failure,
        (
            "anchor = HKQueryAnchor(fromValue: Int(HKAnchoredObjectQueryNoAnchor))",
            "createHeartRateStreamingQuery(date)",
            "if let workout = workoutSession",
            "workoutSession = nil",
            "healthStore.endWorkoutSession(workout)",
            "updateDeviceName(\"\")",
            "updateStatusText(\"cannot start\")",
        ),
    ):
        errors.append("workout query startup must reset admission state and clear failures")

    if failure is None or not ordered(
        failure,
        (
            "if let workout = self.workoutSession",
            "self.workoutSession = nil",
            "self.healthStore.endWorkoutSession(workout)",
            "self.updateDeviceName(\"\")",
            "self.updateStatusText(\"cannot start\")",
        ),
    ):
        errors.append("query failure must clear session ownership and stale source")

    session_failure = function_body(
        source,
        "func workoutSession(workoutSession: HKWorkoutSession, didFailWithError",
        "func workoutDidStart",
    )
    if session_failure is None or not ordered(
        session_failure,
        (
            "self.workoutSession = nil",
            "self.updateDeviceName(\"\")",
            "self.updateStatusText(\"cannot start\")",
        ),
    ):
        errors.append("workout failure must clear stale source before failure status")

    session_end = function_body(source, "func workoutDidEnd", "// MARK: - Actions")
    if session_end is None or not ordered(
        session_end,
        (
            "workoutSession = nil",
            "updateDeviceName(\"\")",
            "updateStatusText(\"---\")",
        ),
    ):
        errors.append("workout end must clear stale source before stopped status")

    return errors
