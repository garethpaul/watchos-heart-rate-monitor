#!/usr/bin/env sh
set -eu
PATH=/usr/bin:/bin
export PATH
ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && /bin/pwd -P)
TEMP_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/watchos-make-authority-XXXXXX")
trap 'rm -rf "$TEMP_ROOT"' EXIT HUP INT TERM
unset MAKEFILES MAKEFILE_LIST MAKEFLAGS MFLAGS MAKEOVERRIDES PYTHON ROOT SHELL XCODEBUILD
CONTROL_DIR="$TEMP_ROOT/control"; CHECKOUT="$TEMP_ROOT/watchos app's [gate] \"quoted\" \`touch WATCHOS_ROOT_MARKER\`"; ATTACKER_ROOT="$TEMP_ROOT/attacker"; AUTHORITY_PATH="$TEMP_ROOT/no-platform-tools"; LOG="$TEMP_ROOT/commands.log"; SHELL_LOG="$TEMP_ROOT/shell.log"
mkdir -p "$CONTROL_DIR" "$CHECKOUT/scripts" "$ATTACKER_ROOT" "$AUTHORITY_PATH"; CONTROL_DIR=$(CDPATH= cd -- "$CONTROL_DIR" && /bin/pwd -P); CHECKOUT=$(CDPATH= cd -- "$CHECKOUT" && /bin/pwd -P); MAKEFILE="$CHECKOUT/Makefile"; cp "$ROOT_DIR/Makefile" "$MAKEFILE"
FAKE_PYTHON="$TEMP_ROOT/trusted python's \"quoted\" \`touch WATCHOS_PYTHON_MARKER\` \$literal"; cat >"$FAKE_PYTHON" <<'EOF'
#!/bin/sh
printf '%s|%s|%s\n' "$PWD" "$0" "$*" >> "$WATCHOS_COMMAND_LOG"
EOF
chmod +x "$FAKE_PYTHON"
for script in test-makefile-root.sh check_watchos_contracts.py test_heart_animation_generation_contract.py test_heart_rate_query_ownership_contract.py test_workflow_contract.py; do cp "$FAKE_PYTHON" "$CHECKOUT/scripts/$script"; done
FAKE_XCODEBUILD="$TEMP_ROOT/trusted xcodebuild"; cat >"$FAKE_XCODEBUILD" <<'EOF'
#!/bin/sh
printf '%s|%s|%s\n' "$PWD" "$0" "$*" >> "$WATCHOS_COMMAND_LOG"
EOF
chmod +x "$FAKE_XCODEBUILD"
FAKE_SHELL="$TEMP_ROOT/fake-shell"; printf '#!/bin/sh\nprintf invoked >> %s\nexec /bin/sh "$@"\n' "'$SHELL_LOG'" >"$FAKE_SHELL"; chmod +x "$FAKE_SHELL"
run_case() { target=$1; mode=$2; output="$TEMP_ROOT/case.out"; rm -f "$LOG" "$SHELL_LOG" "$output"; : >"$CHECKOUT/probe.pyc"; : >"$ATTACKER_ROOT/keep.pyc"; set +e; case "$mode" in default) (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" WATCHOS_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" "XCODEBUILD=$FAKE_XCODEBUILD" "$target") >"$output" 2>&1;; command-root) (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" WATCHOS_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" ROOT="$ATTACKER_ROOT" "PYTHON=$FAKE_PYTHON" "XCODEBUILD=$FAKE_XCODEBUILD" "$target") >"$output" 2>&1;; environment-root) (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" ROOT="$ATTACKER_ROOT" WATCHOS_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" "XCODEBUILD=$FAKE_XCODEBUILD" "$target") >"$output" 2>&1;; command-shell) (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" WATCHOS_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" SHELL="$FAKE_SHELL" "PYTHON=$FAKE_PYTHON" "XCODEBUILD=$FAKE_XCODEBUILD" "$target") >"$output" 2>&1;; environment-shell) (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" SHELL="$FAKE_SHELL" WATCHOS_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" "XCODEBUILD=$FAKE_XCODEBUILD" "$target") >"$output" 2>&1;; esac; status=$?; set -e; if [ "$status" -ne 0 ] || [ -e "$SHELL_LOG" ] || [ ! -e "$ATTACKER_ROOT/keep.pyc" ]; then printf 'authority case failed: target=%s mode=%s status=%s\n' "$target" "$mode" "$status" >&2; cat "$output" >&2; return 1; fi; case "$target" in clean) [ ! -e "$CHECKOUT/probe.pyc" ];; *) grep -Fq "$CHECKOUT" "$LOG";; esac; }
executed=0; for target in build check clean contract-test lint root-test test verify; do for mode in default command-root environment-root command-shell environment-shell; do run_case "$target" "$mode"; executed=$((executed+1)); done; done; [ "$executed" -eq 40 ]
rm -f "$LOG"; (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" WATCHOS_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" "XCODEBUILD=$FAKE_XCODEBUILD" check) >/dev/null 2>&1; grep -Fq "$FAKE_PYTHON" "$LOG"; grep -Fq "$FAKE_XCODEBUILD" "$LOG"; [ ! -e "$CONTROL_DIR/WATCHOS_ROOT_MARKER" ]; [ ! -e "$CONTROL_DIR/WATCHOS_PYTHON_MARKER" ]
MARK="$TEMP_ROOT/python-syntax"; BAD="\$(shell /usr/bin/touch '$MARK')"; if (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" /usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$BAD" lint) >"$TEMP_ROOT/python.out" 2>&1; then exit 1; fi; [ ! -e "$MARK" ]
ENV_MARK="$TEMP_ROOT/python-environment-syntax"; ENV_BAD="\$(shell /usr/bin/touch '$ENV_MARK')"; if (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" PYTHON="$ENV_BAD" /usr/bin/make --environment-overrides --no-print-directory -f "$MAKEFILE" lint) >"$TEMP_ROOT/python-environment.out" 2>&1; then exit 1; fi; [ ! -e "$ENV_MARK" ]
ROOT_MARK="$TEMP_ROOT/root-syntax"; ROOT_BAD="\$(shell /usr/bin/touch '$ROOT_MARK')"; (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" WATCHOS_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" "ROOT=$ROOT_BAD" "PYTHON=$FAKE_PYTHON" XCODEBUILD=/definitely/not-xcodebuild lint) >"$TEMP_ROOT/root.out" 2>&1; [ ! -e "$ROOT_MARK" ]
ROOT_ENV_MARK="$TEMP_ROOT/root-environment-syntax"; ROOT_ENV_BAD="\$(shell /usr/bin/touch '$ROOT_ENV_MARK')"; (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" ROOT="$ROOT_ENV_BAD" WATCHOS_COMMAND_LOG="$LOG" /usr/bin/make --environment-overrides --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" XCODEBUILD=/definitely/not-xcodebuild lint) >"$TEMP_ROOT/root-environment.out" 2>&1; [ ! -e "$ROOT_ENV_MARK" ]
XCODE_MARK="$TEMP_ROOT/xcode-syntax"; XCODE_BAD="\$(shell /usr/bin/touch '$XCODE_MARK')"; if (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" /usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" "XCODEBUILD=$XCODE_BAD" build) >"$TEMP_ROOT/xcode.out" 2>&1; then exit 1; fi; [ ! -e "$XCODE_MARK" ]
XCODE_ENV_MARK="$TEMP_ROOT/xcode-environment-syntax"; XCODE_ENV_BAD="\$(shell /usr/bin/touch '$XCODE_ENV_MARK')"; if (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" XCODEBUILD="$XCODE_ENV_BAD" /usr/bin/make --environment-overrides --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" build) >"$TEMP_ROOT/xcode-environment.out" 2>&1; then exit 1; fi; [ ! -e "$XCODE_ENV_MARK" ]
if (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" /usr/bin/make --no-print-directory -f "$MAKEFILE" MAKEFILE_LIST=/tmp/untrusted check) >"$TEMP_ROOT/list" 2>&1; then exit 1; fi; grep -Fq 'MAKEFILE_LIST must not be overridden' "$TEMP_ROOT/list"
if (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" MAKEFILE_LIST=/tmp/untrusted /usr/bin/make --environment-overrides --no-print-directory -f "$MAKEFILE" check) >"$TEMP_ROOT/list-environment" 2>&1; then exit 1; fi; grep -Fq 'MAKEFILE_LIST must not be overridden' "$TEMP_ROOT/list-environment"
PRE="$TEMP_ROOT/pre.mk"; PRE_MARKER="$TEMP_ROOT/pre-ran"; printf '%s\n' "\$(shell /usr/bin/touch '$PRE_MARKER')" >"$PRE"; if (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" MAKEFILES="$PRE" /usr/bin/make --no-print-directory -f "$MAKEFILE" check) >"$TEMP_ROOT/pre" 2>&1; then exit 1; fi; grep -Fq 'MAKEFILES must be empty' "$TEMP_ROOT/pre"; [ -e "$PRE_MARKER" ]
EARLY="$TEMP_ROOT/early.mk"; EARLY_MARKER="$TEMP_ROOT/early-ran"; printf '%s\n' "\$(shell /usr/bin/touch '$EARLY_MARKER')" >"$EARLY"; if (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" /usr/bin/make --no-print-directory -f "$EARLY" -f "$MAKEFILE" check) >"$TEMP_ROOT/early" 2>&1; then exit 1; fi; [ -s "$TEMP_ROOT/early" ]; [ -e "$EARLY_MARKER" ]
LATER="$TEMP_ROOT/later.mk"; LATER_MARKER="$TEMP_ROOT/later-ran"; cat >"$LATER" <<'LATER_MAKE'
build check clean contract-test lint root-test test verify: MAKEFILE_LIST := Makefile
build check clean contract-test lint root-test test verify:
	@/usr/bin/touch "$$WATCHOS_LATER_MARKER"
LATER_MAKE
for target in build check clean contract-test lint root-test test verify; do
  rm -f "$LATER_MARKER"
  if (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" WATCHOS_LATER_MARKER="$LATER_MARKER" /usr/bin/make --no-print-directory -f "$MAKEFILE" -f "$LATER" "$target" "PYTHON=$FAKE_PYTHON" XCODEBUILD=/definitely/not-xcodebuild) >"$TEMP_ROOT/later-$target" 2>&1; then exit 1; fi
  grep -Fq 'has both : and :: entries' "$TEMP_ROOT/later-$target"
  [ ! -e "$LATER_MARKER" ]
done
LATER_VARS="$TEMP_ROOT/later-vars.mk"; LATER_ROOT_MARKER="$TEMP_ROOT/later-root-ran"; mkdir -p "$ATTACKER_ROOT/scripts"; cat >"$ATTACKER_ROOT/scripts/test-makefile-root.sh" <<'SCRIPT'
#!/bin/sh
/usr/bin/touch "$WATCHOS_LATER_ROOT_MARKER"
SCRIPT
chmod +x "$ATTACKER_ROOT/scripts/test-makefile-root.sh"
TARGET_XCODE="$TEMP_ROOT/target-xcodebuild"; TARGET_XCODE_LOG="$TEMP_ROOT/target-xcode.log"; cat >"$TARGET_XCODE" <<'SCRIPT'
#!/bin/sh
printf '%s\n' "$*" >> "$WATCHOS_TARGET_XCODE_LOG"
exit 0
SCRIPT
chmod +x "$TARGET_XCODE"
cat >"$LATER_VARS" <<LATER_VARS_MAKE
build check clean contract-test lint root-test test verify: MAKEFILE_LIST := $MAKEFILE
build check clean contract-test lint root-test test verify: ROOT := $ATTACKER_ROOT
build check clean contract-test lint root-test test verify: PYTHON := /usr/bin/true
build check clean contract-test lint root-test test verify: XCODEBUILD := $TARGET_XCODE
LATER_VARS_MAKE
rm -f "$LOG" "$LATER_ROOT_MARKER"
if ! (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" WATCHOS_COMMAND_LOG="$LOG" WATCHOS_LATER_ROOT_MARKER="$LATER_ROOT_MARKER" /usr/bin/make --no-print-directory -f "$MAKEFILE" -f "$LATER_VARS" root-test "PYTHON=$FAKE_PYTHON" XCODEBUILD=/definitely/not-xcodebuild) >"$TEMP_ROOT/later-root" 2>&1; then cat "$TEMP_ROOT/later-root" >&2; exit 1; fi
grep -Fq "$CHECKOUT" "$LOG"
[ ! -e "$LATER_ROOT_MARKER" ]
rm -f "$LOG"
if ! (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" WATCHOS_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" -f "$LATER_VARS" lint "PYTHON=$FAKE_PYTHON" XCODEBUILD=/definitely/not-xcodebuild) >"$TEMP_ROOT/later-python" 2>&1; then cat "$TEMP_ROOT/later-python" >&2; exit 1; fi
grep -Fq "$FAKE_PYTHON" "$LOG"
LATER_SHELL="$TEMP_ROOT/later-shell.mk"; LATER_SHELL_LOG="$TEMP_ROOT/later-shell.log"; LATER_FAKE_SHELL="$TEMP_ROOT/later-fake-shell"
cat >"$LATER_FAKE_SHELL" <<'SCRIPT'
#!/bin/sh
printf '%s\n' "$*" >> "$WATCHOS_LATER_SHELL_LOG"
printf '%s\n' ok
exit 0
SCRIPT
chmod +x "$LATER_FAKE_SHELL"
cat >"$LATER_SHELL" <<LATER_SHELL_MAKE
build check clean contract-test lint root-test test verify: MAKEFILE_LIST := $MAKEFILE
build check clean contract-test lint root-test test verify: SHELL := $LATER_FAKE_SHELL
build check clean contract-test lint root-test test verify: .SHELLFLAGS := -c
LATER_SHELL_MAKE
rm -f "$LOG" "$LATER_SHELL_LOG"
if ! (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" WATCHOS_COMMAND_LOG="$LOG" WATCHOS_LATER_SHELL_LOG="$LATER_SHELL_LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" -f "$LATER_SHELL" check "PYTHON=$FAKE_PYTHON" XCODEBUILD=/definitely/not-xcodebuild) >"$TEMP_ROOT/later-shell" 2>&1; then cat "$TEMP_ROOT/later-shell" >&2; exit 1; fi
grep -Fq "$CHECKOUT" "$LOG"
[ ! -e "$LATER_SHELL_LOG" ]
LATER_OVERRIDE="$TEMP_ROOT/later-override.mk"
cat >"$LATER_OVERRIDE" <<LATER_OVERRIDE_MAKE
build check clean contract-test lint root-test test verify: MAKEFILE_LIST := $MAKEFILE
build check clean contract-test lint root-test test verify: override SHELL := $LATER_FAKE_SHELL
build check clean contract-test lint root-test test verify: override .SHELLFLAGS := -c
LATER_OVERRIDE_MAKE
rm -f "$LATER_SHELL_LOG"
(cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" WATCHOS_LATER_SHELL_LOG="$LATER_SHELL_LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" -f "$LATER_OVERRIDE" check "PYTHON=$FAKE_PYTHON" XCODEBUILD=/definitely/not-xcodebuild) >"$TEMP_ROOT/later-override" 2>&1
[ -s "$LATER_SHELL_LOG" ]
PATH_PYTHON="$TEMP_ROOT/python3"; PATH_PYTHON_LOG="$TEMP_ROOT/path-python.log"; cp "$FAKE_PYTHON" "$PATH_PYTHON"
rm -f "$PATH_PYTHON_LOG"
(cd "$CONTROL_DIR"&&PATH="$TEMP_ROOT:/usr/bin:/bin" WATCHOS_COMMAND_LOG="$PATH_PYTHON_LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" lint) >"$TEMP_ROOT/path-python" 2>&1
[ -s "$PATH_PYTHON_LOG" ]
PATH_XCODE="$TEMP_ROOT/xcodebuild"; PATH_XCODE_LOG="$TEMP_ROOT/path-xcode.log"; cat >"$PATH_XCODE" <<'SCRIPT'
#!/bin/sh
printf '%s\n' "$*" >> "$WATCHOS_PATH_XCODE_LOG"
exit 0
SCRIPT
chmod +x "$PATH_XCODE"
rm -f "$PATH_XCODE_LOG"
(cd "$CONTROL_DIR"&&PATH="$TEMP_ROOT:/usr/bin:/bin" WATCHOS_PATH_XCODE_LOG="$PATH_XCODE_LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" build "PYTHON=$FAKE_PYTHON" XCODEBUILD=/definitely/not-xcodebuild) >"$TEMP_ROOT/path-xcode" 2>&1
[ ! -e "$PATH_XCODE_LOG" ]
EXPLICIT_XCODE="$TEMP_ROOT/explicit xcodebuild"; EXPLICIT_XCODE_LOG="$TEMP_ROOT/explicit-xcode.log"; cat >"$EXPLICIT_XCODE" <<'SCRIPT'
#!/bin/sh
printf '%s\n' "$*" >> "$WATCHOS_EXPLICIT_XCODE_LOG"
exit 0
SCRIPT
chmod +x "$EXPLICIT_XCODE"
rm -f "$EXPLICIT_XCODE_LOG" "$TARGET_XCODE_LOG"
(cd "$CONTROL_DIR"&&PATH="$TEMP_ROOT:/usr/bin:/bin" XCODEBUILD="$EXPLICIT_XCODE" WATCHOS_EXPLICIT_XCODE_LOG="$EXPLICIT_XCODE_LOG" WATCHOS_TARGET_XCODE_LOG="$TARGET_XCODE_LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" -f "$LATER_VARS" build "PYTHON=$FAKE_PYTHON") >"$TEMP_ROOT/explicit-xcode" 2>&1
[ -s "$EXPLICIT_XCODE_LOG" ]
[ ! -e "$TARGET_XCODE_LOG" ]
if (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" /usr/bin/make --no-print-directory -f "$MAKEFILE" MAKEFLAGS=-n check) >"$TEMP_ROOT/flags" 2>&1; then exit 1; fi; grep -Fq 'MAKEFLAGS must not be overridden' "$TEMP_ROOT/flags"
for flag in -n --just-print --dry-run --recon -t --touch -q --question -i --ignore-errors; do if (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" /usr/bin/make "$flag" --no-print-directory -f "$MAKEFILE" check) >"$TEMP_ROOT/flag" 2>&1; then exit 1; fi; grep -Fq 'non-executing or error-ignoring MAKEFLAGS are not supported' "$TEMP_ROOT/flag"; done
printf '%s\n' 'Make authority tests passed: 40 target/authority cases, literal hostile Python path, 6 raw Make-syntax controls, 2 MAKEFILE_LIST rejections, 2 startup-boundary cases, 8 later recipe-replacement rejections, later root/Python/Xcode and non-override shell protection, override/startup/PATH-Python boundary controls, PATH-Xcode rejection, cleanup containment, caller MAKEFLAGS rejection, and 10 mode rejections'
