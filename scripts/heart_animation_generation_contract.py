#!/usr/bin/env python3
"""Static contract for generation-bound WatchKit heart animations."""


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

    if "var heartAnimationGeneration = 0" not in source:
        errors.append("heart animation generation state must be retained")

    reset = function_body(source, "func resetHeartAnimation()", "func animateHeart()")
    if reset is None or not ordered(
        reset,
        (
            "heartAnimationGeneration += 1",
            "heart.setWidth(50)",
            "heart.setHeight(80)",
        ),
    ):
        errors.append("heart animation reset must invalidate callbacks before restoring size")

    animate = function_body(source, "func animateHeart()", "\n}")
    if animate is None:
        errors.append("heart animation method must remain present")
    else:
        preamble, separator, delayed = animate.partition("dispatch_after(when, queue)")
        if not separator or not ordered(
            preamble,
            (
                "guard interfaceActive else {return}",
                "guard workoutActive else {return}",
                "heartAnimationGeneration += 1",
                "let animationGeneration = heartAnimationGeneration",
                "self.heart.setWidth(60)",
            ),
        ):
            errors.append("heart expansion must require active interface and workout ownership")
        if not separator or not ordered(
            delayed,
            (
                "dispatch_async(dispatch_get_main_queue()",
                "guard self.interfaceActive else {return}",
                "guard self.workoutActive else {return}",
                "guard self.heartAnimationGeneration == animationGeneration else {return}",
                "self.heart.setWidth(50)",
            ),
        ):
            errors.append("delayed heart animation must recheck interface, workout, and generation state")

    teardown_methods = (
        ("override func didDeactivate()", "func displayAuthorizationFailed()", ("interfaceActive = false", "authorizationGeneration += 1", "resetHeartAnimation()")),
        ("func workoutSession(workoutSession: HKWorkoutSession, didFailWithError", "func workoutDidStart", ("self.workoutActive = false", "self.resetHeartAnimation()")),
        ("func workoutDidStart", "func workoutDidEnd", ("workoutActive = false", "resetHeartAnimation()")),
        ("func workoutDidEnd", "// MARK: - Actions", ("workoutActive = false", "resetHeartAnimation()")),
        ("@IBAction func startBtnTapped()", "func startWorkout()", ("self.workoutActive = false", "self.resetHeartAnimation()")),
        ("func heartRateQueryDidFail", "func updateHeartRate", ("self.workoutActive = false", "self.resetHeartAnimation()")),
    )
    for start_marker, end_marker, fragments in teardown_methods:
        body = function_body(source, start_marker, end_marker)
        if body is None or not ordered(body, fragments):
            errors.append("{0} must invalidate lifecycle state before resetting heart animation".format(start_marker))

    return errors
