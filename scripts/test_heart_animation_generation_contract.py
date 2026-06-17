#!/usr/bin/env python3
"""Mutation tests for generation-bound WatchKit heart animations."""

from pathlib import Path

from heart_animation_generation_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "HeartyMonitor WatchKit Extension" / "InterfaceController.swift"


def main():
    source = SOURCE.read_text(encoding="utf-8")
    errors = validation_errors(source)
    if errors:
        raise AssertionError("baseline heart animation contract failed: " + "; ".join(errors))

    mutations = {
        "remove generation state": source.replace("    var heartAnimationGeneration = 0\n", "", 1),
        "remove deactivation reset": source.replace("        resetHeartAnimation()\n        super.didDeactivate()", "        super.didDeactivate()", 1),
        "remove workout failure reset": source.replace("            guard self.workoutSession === workoutSession else { return }\n            self.workoutActive = false\n            self.resetHeartAnimation()", "            guard self.workoutSession === workoutSession else { return }\n            self.workoutActive = false", 1),
        "remove query creation reset": source.replace("            resetHeartAnimation()\n            startStopButton.setTitle(\"Start\")", "            startStopButton.setTitle(\"Start\")", 1),
        "remove ended reset": source.replace("        resetHeartAnimation()\n        startStopButton.setTitle(\"Start\")", "        startStopButton.setTitle(\"Start\")", 1),
        "remove user stop reset": source.replace("            //finish the current workout\n            self.workoutActive = false\n            self.resetHeartAnimation()", "            //finish the current workout\n            self.workoutActive = false", 1),
        "remove query error reset": source.replace("            guard self.heartRateQuery === query else {return}\n            self.workoutActive = false\n            self.resetHeartAnimation()", "            guard self.heartRateQuery === query else {return}\n            self.workoutActive = false", 1),
        "reset before workout deactivation": source.replace("            //finish the current workout\n            self.workoutActive = false\n            self.resetHeartAnimation()", "            //finish the current workout\n            self.resetHeartAnimation()\n            self.workoutActive = false", 1),
        "remove expansion interface guard": source.replace("        guard interfaceActive else {return}\n", "", 1),
        "remove expansion workout guard": source.replace("        guard workoutActive else {return}\n", "", 1),
        "remove delayed interface guard": source.replace("                guard self.interfaceActive else {return}\n", "", 1),
        "remove delayed workout guard": source.replace("                guard self.workoutActive else {return}\n", "", 1),
        "remove delayed generation guard": source.replace("                guard self.heartAnimationGeneration == animationGeneration else {return}\n", "", 1),
        "capture generation after expansion": source.replace("        let animationGeneration = heartAnimationGeneration\n", "", 1).replace("            self.heart.setHeight(90)\n", "            self.heart.setHeight(90)\n            let animationGeneration = heartAnimationGeneration\n", 1),
    }

    for name, mutated_source in mutations.items():
        if not validation_errors(mutated_source):
            raise AssertionError("mutation was not rejected: " + name)

    print("heart animation generation mutations rejected ({0} cases)".format(len(mutations)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
