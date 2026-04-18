#!/usr/bin/env python3
"""Plan-review gate verifier. Checks filesystem artifacts from dispatched reviewers.

Exit 0 = allow (no stdout). Exit 2 = deny (JSON on stdout).
Called by verify-plan-reviews.sh trampoline.
"""
import hashlib
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import NoReturn

PLANS_DIR = Path(os.environ.get("PLANS_DIR", os.path.expanduser("~/.claude/plans")))
REVIEWS_DIR = Path(os.environ.get("REVIEWS_DIR", os.path.expanduser("~/.claude/plan-reviews")))
AGENT_FILE_PATTERN = re.compile(r"-agent-")
PLAN_FILENAME_RE = re.compile(r"^[A-Za-z0-9._-]+\.md$")
ROUND_DIR_RE = re.compile(r"^round-(\d+)$")
CLEANUP_AGE_DAYS = 14
VERDICT_PASS = "PASS"
VERDICT_FAIL = "FAIL"
REQUIRED_KEYS = {"agent", "critical", "verdict"}


def deny(reason: str) -> NoReturn:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"GATE: {reason}",
    }}))
    sys.exit(2)


def extract_frontmatter(content: str) -> dict | str:
    stripped = content.rstrip()
    if not stripped.endswith("---"):
        return "file does not end with '---' fence (trailing commentary?)"
    lines = stripped.split("\n")
    if len(lines) < 5:
        return "file too short for 5-line verdict block"
    block = lines[-5:]
    if block[0] != "---" or block[4] != "---":
        return "final 5 lines are not a fenced block"
    fields: dict[str, str] = {}
    for line in block[1:4]:
        m = re.match(r"^([A-Za-z]+):\s*(.+?)\s*$", line)
        if not m:
            return f"malformed frontmatter line: {line!r}"
        key = m.group(1).lower()
        value = m.group(2)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        if key in fields:
            return f"duplicate key: {key}"
        fields[key] = value
    if set(fields.keys()) != REQUIRED_KEYS:
        return f"keys {sorted(fields.keys())} != required {sorted(REQUIRED_KEYS)}"
    return fields


def validate_fields(fields: dict) -> str | None:
    try:
        crit = int(fields["critical"])
    except ValueError:
        return f"critical is not an integer: {fields['critical']!r}"
    if crit < 0:
        return f"critical is negative: {crit}"
    verdict = fields["verdict"]
    if verdict not in (VERDICT_PASS, VERDICT_FAIL):
        return f"verdict must be PASS or FAIL, got: {verdict!r}"
    if (verdict == VERDICT_PASS) != (crit == 0):
        return f"verdict/critical inconsistency: verdict={verdict}, critical={crit}"
    if not fields["agent"].strip():
        return "agent field is empty"
    return None


def normalize(content: str) -> str:
    return "\n".join(line.rstrip() for line in content.splitlines()) + "\n"


def identify_plan(stdin_data: str) -> tuple[Path, str]:
    try:
        payload = json.loads(stdin_data) if stdin_data.strip() else {}
        plan_content = payload.get("tool_input", {}).get("plan", "")
    except (json.JSONDecodeError, AttributeError):
        plan_content = ""

    candidates = [
        p for p in sorted(PLANS_DIR.glob("*.md"))
        if not AGENT_FILE_PATTERN.search(p.stem)
    ]

    if plan_content:
        target_hash = hashlib.sha256(normalize(plan_content).encode()).hexdigest()
        matches = [
            p for p in candidates
            if hashlib.sha256(normalize(p.read_text()).encode()).hexdigest() == target_hash
        ]
        if len(matches) == 1:
            return matches[0], "content-hash"

    if not candidates:
        deny("Could not locate any plan file in " + str(PLANS_DIR))

    plan = max(candidates, key=lambda p: p.stat().st_mtime)
    return plan, "mtime-fallback"


def cleanup_old_reviews() -> None:
    if not REVIEWS_DIR.exists():
        return
    sentinel = REVIEWS_DIR / ".last-cleanup"
    # Only run cleanup once per day
    if sentinel.exists() and (time.time() - sentinel.stat().st_mtime) < 86400:
        return
    cutoff = time.time() - (CLEANUP_AGE_DAYS * 86400)
    for slug_dir in REVIEWS_DIR.iterdir():
        if not slug_dir.is_dir():
            continue
        if slug_dir.stat().st_mtime > cutoff:
            continue
        newest = 0.0
        for f in slug_dir.rglob("*"):
            if f.is_file():
                newest = max(newest, f.stat().st_mtime)
        if newest > 0 and newest < cutoff:
            shutil.rmtree(slug_dir)
    try:
        sentinel.touch()
    except OSError:
        pass


def last_n_lines(content: str, n: int = 10, max_chars: int = 400) -> str:
    lines = content.splitlines()
    snippet = "\n".join(lines[-n:])
    return snippet[:max_chars]


def run() -> None:
    stdin_data = sys.stdin.read()

    cleanup_old_reviews()

    plan_path, id_tag = identify_plan(stdin_data)

    if not PLAN_FILENAME_RE.match(plan_path.name):
        deny(f"(via {id_tag}) plan filename must match [A-Za-z0-9._-]+, got: {plan_path.name!r}")

    slug = plan_path.stem
    review_root = REVIEWS_DIR / slug

    if not review_root.is_dir():
        deny(
            f"This plan has no review artifacts at {review_root}/. "
            f"(plan identified via {id_tag})\n\n"
            "Before calling ExitPlanMode:\n"
            f"1. Create {review_root}/round-1/.\n"
            "2. Dispatch 3+ reviewer agents. See CLAUDE.md Planning.\n"
            "3. Paste reviewer-template.txt verbatim in each dispatch.\n"
            f"4. Save responses to {review_root}/round-1/<agent-slug>-<index>.md.\n"
            "5. If any verdict: FAIL, fix plan, create round-2/, dispatch again.\n"
            "6. When latest round is all PASS, call ExitPlanMode."
        )

    if (review_root / "WAIVED").is_file():
        return

    rounds: list[int] = []
    for entry in review_root.iterdir():
        m = ROUND_DIR_RE.match(entry.name)
        if m and entry.is_dir():
            rounds.append(int(m.group(1)))

    if not rounds:
        deny(f"No round directories in {review_root}/. Create round-1/ and populate it. "
             f"(plan identified via {id_tag})")

    latest = max(rounds)
    latest_dir = review_root / f"round-{latest}"

    md_files = sorted(latest_dir.glob("*.md"))
    if len(md_files) < 3:
        deny(f"Only {len(md_files)} review file(s) in round-{latest}; need 3+. "
             f"Dispatch more reviewers into {latest_dir}/. "
             f"(plan identified via {id_tag})")

    errors: list[str] = []
    failures: list[str] = []

    for f in md_files:
        content = f.read_text()
        result = extract_frontmatter(content)

        if isinstance(result, str):
            snippet = last_n_lines(content)
            errors.append(f"{f.name}: {result}\n  Last lines:\n  {snippet}")
            continue

        err = validate_fields(result)
        if err:
            errors.append(f"{f.name}: {err}")
            continue

        if result["verdict"] == VERDICT_FAIL:
            failures.append(f.name)

    if errors:
        error_list = "\n".join(f"  - {e}" for e in errors)
        deny(f"Malformed review file(s) in round-{latest}:\n{error_list}\n"
             f"(plan identified via {id_tag})")

    if failures:
        fail_list = ", ".join(failures)
        deny(f"verdict: FAIL in round-{latest} from: {fail_list}. "
             f"Fix the plan, create round-{latest + 1}/, dispatch reviewers again. "
             f"(plan identified via {id_tag})")


def main() -> None:
    try:
        run()
    except SystemExit:
        raise
    except Exception as e:
        deny(f"verifier internal error: {type(e).__name__}: {str(e)[:500]}")


if __name__ == "__main__":
    main()
