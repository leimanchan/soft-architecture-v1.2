#!/usr/bin/env python3
"""Fail if core contains filesystem or process side effects."""

from __future__ import annotations

from pathlib import Path

FORBIDDEN_CALLS = [
    "open(",
    ".open(",
    "read_text(",
    "write_text(",
    "mkdir(",
    "rglob(",
    "glob(",
    "iterdir(",
    "unlink(",
    "rename(",
    "replace(",
    "rmdir(",
    "chmod(",
    "touch(",
    "exists(",
    "stat(",
    "lstat(",
    "walk(",
    "listdir(",
    "remove(",
    "makedirs(",
    "mkdtemp(",
    "mkstemp(",
    "Popen(",
    "subprocess.",
    "socket.",
]


def scan_file(path: Path) -> list[str]:
    violations = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return violations

    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        for token in FORBIDDEN_CALLS:
            if token in stripped:
                violations.append(f"{path}:{i}: forbidden IO call '{token}'")
    return violations


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    core_dir = root / "core"
    if not core_dir.exists():
        print("core/ not found")
        return 1

    violations: list[str] = []
    for path in core_dir.rglob("*.py"):
        violations.extend(scan_file(path))

    if violations:
        print("Core IO purity check failed:")
        for v in violations:
            print(f"- {v}")
        return 1

    print("Core IO purity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
