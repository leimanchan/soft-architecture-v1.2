#!/usr/bin/env python3
"""Enforce adapter edits only after required core artifacts exist."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

SCOPES = ("staged", "working-tree", "both")


def _git_paths(root: Path, scope: str) -> list[str] | None:
    if scope == "staged":
        cmd = ["git", "diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR"]
        skip_msg = "Adapter sequencing check skipped (not a git repo)."
    else:
        cmd = ["git", "status", "--porcelain=v1", "-z"]
        skip_msg = "Adapter guard skipped (not a git repo)."

    result = subprocess.run(
        cmd,
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(skip_msg)
        return None

    entries = [e for e in result.stdout.split("\0") if e]
    if scope == "staged":
        return entries

    paths: list[str] = []
    i = 0
    while i < len(entries):
        entry = entries[i]
        if len(entry) >= 3:
            status = entry[:2]
            path_part = entry[3:]
            if status.startswith("R") or status.startswith("C"):
                if i + 1 < len(entries):
                    paths.append(entries[i + 1])
                    i += 2
                    continue
            paths.append(path_part.strip())
        i += 1
    return paths


def _adapter_tools(paths: list[str]) -> set[str]:
    tools = set()
    for path in paths:
        parts = path.split("/")
        if len(parts) >= 3 and parts[0] == "adapters" and parts[2] != "_base":
            tools.add(parts[2])
    return tools


def _missing_core_artifacts(root: Path, tool: str) -> list[Path]:
    core_dir = root / "core" / tool
    required = [
        core_dir / "DECISIONS.md",
        core_dir / "domain" / "models.py",
        core_dir / "domain" / "specs.py",
        core_dir / "contracts.py",
        core_dir / "application" / "orchestrator.py",
    ]
    missing = [p for p in required if not p.exists()]
    tests_dir = core_dir / "tests"
    test_files = list(tests_dir.glob("test_*.py")) if tests_dir.exists() else []
    if not tests_dir.exists() or not test_files:
        missing.append(tests_dir / "test_*.py")
    return missing


def _collect_tools(root: Path, scope: str) -> set[str] | None:
    if scope in {"staged", "working-tree"}:
        paths = _git_paths(root, scope)
        if paths is None:
            return None
        return _adapter_tools(paths)

    staged_paths = _git_paths(root, "staged")
    if staged_paths is None:
        return None
    working_paths = _git_paths(root, "working-tree")
    if working_paths is None:
        return None
    return _adapter_tools(staged_paths + working_paths)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", choices=SCOPES, default="both")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    tools = _collect_tools(root, args.scope)
    if tools is None:
        return 0

    if not tools:
        print("Adapter sequencing check passed.")
        return 0

    failures = []
    for tool in sorted(tools):
        missing = _missing_core_artifacts(root, tool)
        if missing:
            failures.append((tool, missing))

    if failures:
        print(f"Adapter changes detected before core artifacts exist ({args.scope}):")
        for tool, missing in failures:
            print(f"- {tool} missing:")
            for path in missing:
                print(f"  - {path}")
        return 1

    print("Adapter sequencing check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
