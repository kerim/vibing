#!/bin/sh
set -u
# set -e deliberately omitted: we need STATUS=$? to capture non-zero exits
# from python3 so we can emit the crash-path deny. Adding set -e would abort
# the script before STATUS capture and break fail-closed behavior.
trap 'exit 2' INT TERM HUP

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$SCRIPT_DIR/verify-plan-reviews.py"

if [ ! -f "$SCRIPT" ] || [ ! -x "$SCRIPT" ]; then
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"GATE: verifier script missing or not executable. Reinstall the hook."}}\n'
    exit 2
fi

/usr/bin/env python3 "$SCRIPT"
STATUS=$?

if [ "$STATUS" -eq 0 ] || [ "$STATUS" -eq 2 ]; then
    exit "$STATUS"
fi

if [ "$STATUS" -eq 127 ]; then
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"GATE: python3 not found in PATH - install Python 3"}}\n'
else
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"GATE: verifier script crashed with exit %d - check logs"}}\n' "$STATUS"
fi
exit 2
