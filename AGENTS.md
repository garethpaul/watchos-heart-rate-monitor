# AGENTS.md

## Repository purpose

`garethpaul/watchos-heart-rate-monitor` is an Apple platform application or Swift sample. HRM for WatchOS

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `HeartyMonitor.xcodeproj` - Xcode project
- `HeartyMonitor` - repository source or sample assets
- `HeartyMonitor WatchKit App` - repository source or sample assets
- `HeartyMonitor WatchKit Extension` - repository source or sample assets
- `HeartyMonitorTests` - repository source or sample assets
- `HeartyMonitorUITests` - repository source or sample assets

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check`
- Combined verification: `make verify`
- Lint/static checks: `make lint`
- Workflow contract mutations: `make contract-test`
- Tests: `make test`
- Build: `make build`
- Local Apple development: `open HeartyMonitor.xcodeproj`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Swift (13).
- Preserve legacy Xcode project settings and signing assumptions unless the change is explicitly about modernization.

## Testing guidance

- Test-related files detected: `docs/plans/2026-06-08-watchkit-uitest-query-mirror.md`, `HeartyMonitorTests/HeartyMonitorTests.swift`, `HeartyMonitorUITests/HeartyMonitorTests/HeartyMonitorTests.swift`, `HeartyMonitorUITests/HeartyMonitorUITests.swift`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.
- Keep hosted verification read-only and credential-free with immutable action
  pins; update structural workflow mutations with intentional policy changes.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.
- HealthKit read access uses `NSHealthShareUsageDescription` to explain that the sample reads heart-rate data for live workout feedback.
- HealthKit authorization callback success means the request was processed; it
  does not reveal whether the user granted read access. Do not infer or display
  a read-denial state from that callback.
- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-26-healthkit-setup-guide.md` for the source-backed
  HealthKit target, entitlement, signing, and historical version setup boundary.
- See `docs/plans/2026-06-08-healthkit-privacy-strings.md` for the current HealthKit privacy and query baseline.
- Delayed heart animations must match the current interface, workout, and
  animation generation before changing WatchKit UI.
- Each workout must reset its anchored-query cursor and admit only samples whose
  start date belongs to that workout.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
