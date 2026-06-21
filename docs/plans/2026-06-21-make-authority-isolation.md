# Isolate Make, Python, and Xcode Verification Authority

## Status: Completed

## Context

The Makefile rooted cleanup and static checks at its own location, but callers
could still replace the recipe shell, load startup makefiles, override the
Makefile list, select non-executing or error-ignoring modes, embed Make syntax
in executable values, or append single-colon public recipes after the reviewed
file.

## Requirements

- Derive the repository root only from the reviewed Makefile path.
- Freeze literal Python and Xcode executable values without evaluating Make
  syntax, including paths with spaces and shell metacharacters.
- Fix ordinary public recipes to `/bin/sh`, reject injected startup files and
  replaced Makefile lists, and reject unsafe execution modes.
- Reject later single-colon replacement of every public target while
  preserving the documented caller-override boundary.
- Keep bytecode cleanup confined to the reviewed repository before and after
  the full gate.
- Exercise all eight public targets under command-line and environment root
  and shell attacks, plus PATH and later-makefile attacks.
- Invoke hosted verification through `/usr/bin/make`.

## Scope Boundaries

- Do not change HealthKit, workout, query, animation, UI, project, entitlement,
  deployment, or physical-device behavior.
- Preserve the static-only hosted policy and truthful local Xcode skip.
- Caller-supplied GNU Make `override` directives and PATH selection of the
  default `python3` remain explicit boundaries rather than claimed prevention.

## Verification

- Repository and external-directory `make check` passed 25 static checks, 14
  heart-animation mutations, 12 query-ownership mutations, and 17 workflow
  mutations; Xcode was truthfully unavailable on Linux.
- The authority harness passed 40 public-target/root/shell cases, six raw
  Make-syntax controls, two Makefile-list rejections, two startup boundaries,
  eight later recipe-replacement rejections, later root/Python/Xcode and shell
  controls, PATH-Xcode rejection, cleanup containment, caller `MAKEFLAGS`, and
  ten unsafe-mode rejections.
- Python and shell syntax, workflow YAML, project/plist parsing,
  `git diff --check`, intended-path, artifact, and changed-line credential
  audits passed.
