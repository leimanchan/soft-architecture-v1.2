#!/usr/bin/env python3
"""Block adapter changes if core artifacts do not exist (working tree)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print("Failed to read git status")
        return 1

    changed = []
    for line in result.stdout.splitlines():
        path = line[3:].strip()
        if path.startswith("adapters/"):
            changed.append(path)

    tools = set()
    for path in changed:
        parts = path.split("/")
        if len(parts) >= 3 and parts[0] == "adapters":
            if parts[2] != "_base":
                tools.add(parts[2])

    if not tools:
        print("Adapter guard passed.")
        return 0

    failures = []
    for tool in sorted(tools):
        core_dir = root / "core" / tool
        required = [
            core_dir / "DECISIONS.md",
            core_dir / "domain" / "models.py",
            core_dir / "domain" / "specs.py",
            core_dir / "contracts.py",
            core_dir / "application" / "service.py",
            core_dir / "application" / "orchestrator.py",
        ]
        missing = [p for p in required if not p.exists()]
        if missing:
            failures.append((tool, missing))

    if failures:
        print("Adapter changes detected before core artifacts exist (working tree):")
        for tool, missing in failures:
            print(f"- {tool} missing:")
            for p in missing:
                print(f"  - {p}")
        return 1

    print("Adapter guard passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
