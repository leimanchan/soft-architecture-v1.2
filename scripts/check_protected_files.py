#!/usr/bin/env python3
"""Block edits to deterministic governance files unless explicitly allowed."""

from __future__ import annotations

import fnmatch
import os
import subprocess
from pathlib import Path

PROTECTED_PATTERNS = (
    "tests/test_enforcement_flow.py",
    "scripts/check_*.py",
    "scripts/preflight.py",
    "scripts/preflight_core.py",
    "scripts/preflight_local.py",
    "scripts/runtime_gate.py",
    ".github/workflows/preflight.yml",
)

OVERRIDE_ENV = "ALLOW_PROTECTED_CHANGES"


def _run_git(root: Path, args: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode, output.strip()


def _is_git_repo(root: Path) -> bool:
    code, output = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    return code == 0 and output == "true"


def _split_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def _changed_files_local(root: Path) -> list[str]:
    changed: set[str] = set()
    commands = [
        ["diff", "--name-only", "--diff-filter=ACMRD"],
        ["diff", "--cached", "--name-only", "--diff-filter=ACMRD"],
        ["ls-files", "--others", "--exclude-standard"],
    ]
    for args in commands:
        code, output = _run_git(root, args)
        if code == 0:
            changed.update(_split_lines(output))
    return sorted(changed)


def _changed_files_ci(root: Path) -> list[str] | None:
    base_ref = os.environ.get("GITHUB_BASE_REF", "").strip()
    before_sha = os.environ.get("GITHUB_EVENT_BEFORE", "").strip()

    if base_ref:
        _run_git(root, ["fetch", "origin", base_ref, "--depth=1"])
        code, output = _run_git(root, ["diff", "--name-only", f"origin/{base_ref}...HEAD", "--diff-filter=ACMRD"])
        if code == 0:
            return sorted(set(_split_lines(output)))

    if before_sha and before_sha != "0" * 40:
        code, output = _run_git(root, ["diff", "--name-only", f"{before_sha}...HEAD", "--diff-filter=ACMRD"])
        if code == 0:
            return sorted(set(_split_lines(output)))

    return None


def _matches_protected(path: str) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in PROTECTED_PATTERNS)


def _override_patterns() -> list[str]:
    value = os.environ.get(OVERRIDE_ENV, "").strip()
    if not value:
        return []
    if value == "1":
        return ["*"]
    return [part.strip() for part in value.split(",") if part.strip()]


def _is_override_allowed(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    if not _is_git_repo(root):
        print("Protected file check skipped: not a git repo.")
        return 0

    override_patterns = _override_patterns()
    if override_patterns == ["*"]:
        print(f"Protected file check bypassed via {OVERRIDE_ENV}=1.")
        return 0

    changed_files: list[str]
    if os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"):
        ci_files = _changed_files_ci(root)
        changed_files = ci_files if ci_files is not None else _changed_files_local(root)
    else:
        changed_files = _changed_files_local(root)

    violations = [
        path
        for path in changed_files
        if _matches_protected(path) and not _is_override_allowed(path, override_patterns)
    ]
    if violations:
        print("Protected governance files were modified:")
        for path in violations:
            print(f"- {path}")
        print("")
        print(
            "Deterministic tests/checks are immutable during normal agent work. "
            f"Human override only: set {OVERRIDE_ENV}=1 (global) or {OVERRIDE_ENV}=<glob>[,<glob>...] (scoped)."
        )
        return 1

    if override_patterns:
        print(f"Protected file check passed with scoped override: {OVERRIDE_ENV}={','.join(override_patterns)}")
        return 0

    print("Protected file check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
