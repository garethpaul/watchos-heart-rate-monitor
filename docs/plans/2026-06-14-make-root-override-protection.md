# Protect the Make Repository Root from Overrides

## Status: Planned

## Context

The Makefile-derived repository root anchors portable HealthKit contracts,
workflow mutations, cleanup, and optional Xcode builds, but an ordinary `:=`
assignment can be replaced from the command line.

## Requirements

- Protect the Makefile-derived `ROOT` with GNU Make's `override` directive.
- Preserve configurable `PYTHON` and `XCODEBUILD` commands.
- Require exact protected root and tool override lines in the checker.
- Pass local, external-directory, and hostile-root full gates.
- Reject weakened root, checker, tool override, cleanup, and plan mutations.
- Preserve HealthKit, mirrored-source, workflow, and project contracts.

## Verification Plan

- focused CI/Makefile contract and Python compilation
- bounded local, external-directory, and hostile-root `make check`
- focused mutations
- workflow YAML, plist/storyboard/workspace XML, mirror parity, artifact,
  whitespace, and changed-line secret audits

## Scope Boundaries

- Do not alter Swift behavior, project files, workflows, or HealthKit policy.
- Do not merge or close stacked pull requests without owner authorization.
