#!/usr/bin/env python3
"""Mutation tests for main-queue-owned HealthKit query state."""

from pathlib import Path

from heart_rate_query_ownership_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "HeartyMonitor WatchKit Extension" / "InterfaceController.swift"


def main():
    source = SOURCE.read_text(encoding="utf-8")
    errors = validation_errors(source)
    if errors:
        raise AssertionError("baseline query ownership contract failed: " + "; ".join(errors))

    mutations = {
        "remove initial main dispatch": source.replace(
            "            dispatch_async(dispatch_get_main_queue()) {\n                self.handleHeartRateQueryResult(query, samples: sampleObjects, newAnchor: newAnchor, error: error)\n            }\n",
            "            self.handleHeartRateQueryResult(query, samples: sampleObjects, newAnchor: newAnchor, error: error)\n",
            1,
        ),
        "remove update main dispatch": source.replace(
            "            dispatch_async(dispatch_get_main_queue()) {\n                self.handleHeartRateQueryResult(query, samples: samples, newAnchor: newAnchor, error: error)\n            }\n",
            "            self.handleHeartRateQueryResult(query, samples: samples, newAnchor: newAnchor, error: error)\n",
            1,
        ),
        "remove current query guard": source.replace(
            "        guard heartRateQuery === query else {return}\n",
            "",
            1,
        ),
        "advance anchor before identity": source.replace(
            "        guard heartRateQuery === query else {return}\n",
            "        anchor = newAnchor!\n        guard heartRateQuery === query else {return}\n",
            1,
        ),
        "remove status interface guard": source.replace(
            "        guard interfaceActive else {return}\n",
            "",
            1,
        ),
        "accept zero heart rate": source.replace(
            "        guard value > 0 && value <= 300 else{return}\n",
            "        guard value >= 0 && value <= 300 else{return}\n",
            1,
        ),
        "render before animation reset": source.replace(
            "        resetHeartAnimation()\n        renderInterfaceState()\n",
            "        renderInterfaceState()\n        resetHeartAnimation()\n",
            1,
        ),
        "retain ending workout session": source.replace(
            "                self.workoutSession = nil\n                healthStore.endWorkoutSession(workout)\n",
            "                healthStore.endWorkoutSession(workout)\n",
            1,
        ),
        "retain stopped source": source.replace(
            "            self.updateStatusText(\"---\")\n            self.updateDeviceName(\"\")\n",
            "            self.updateStatusText(\"---\")\n",
            1,
        ),
        "end failed query session before clearing": source.replace(
            "                workoutSession = nil\n                healthStore.endWorkoutSession(workout)\n",
            "                healthStore.endWorkoutSession(workout)\n                workoutSession = nil\n",
            1,
        ),
        "retain failed workout source": source.replace(
            "            self.workoutSession = nil\n            self.updateDeviceName(\"\")\n            self.updateStatusText(\"cannot start\")\n",
            "            self.workoutSession = nil\n            self.updateStatusText(\"cannot start\")\n",
            1,
        ),
        "retain ended workout source": source.replace(
            "        workoutSession = nil\n        updateDeviceName(\"\")\n        updateStatusText(\"---\")\n",
            "        workoutSession = nil\n        updateStatusText(\"---\")\n",
            1,
        ),
    }

    for name, mutated_source in mutations.items():
        if not validation_errors(mutated_source):
            raise AssertionError("mutation was not rejected: " + name)

    print("heart-rate query ownership mutations rejected ({0} cases)".format(len(mutations)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
