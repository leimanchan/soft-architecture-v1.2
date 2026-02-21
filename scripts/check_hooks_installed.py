#!/usr/bin/env python3
"""Ensure pre-commit hook is installed and runs preflight."""

from __future__ import annotations

from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    hook = root / ".git" / "hooks" / "pre-commit"
    if not hook.exists():
        print("pre-commit hook not installed")
        return 1
    text = hook.read_text(encoding="utf-8", errors="ignore")
    if "scripts/preflight.py" not in text:
        print("pre-commit hook does not run preflight.py")
        return 1
    print("Hook check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
