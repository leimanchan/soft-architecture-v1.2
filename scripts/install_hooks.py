#!/usr/bin/env python3
"""Install git hooks for this repo."""

from __future__ import annotations

from pathlib import Path

HOOK = """#!/bin/sh
set -e

ROOT_DIR=$(git rev-parse --show-toplevel)
PYTHON_EXEC="${PYTHON_EXECUTABLE:-}"
if [ -z "$PYTHON_EXEC" ] && [ -x "$ROOT_DIR/.venv/bin/python" ]; then
  PYTHON_EXEC="$ROOT_DIR/.venv/bin/python"
fi
if [ -z "$PYTHON_EXEC" ]; then
  PYTHON_EXEC="python3"
fi

"$PYTHON_EXEC" "$ROOT_DIR/scripts/preflight.py"

# If new tools were added under core/, enforce soft checkpoints for each.
NEW_TOOLS=$(git diff --cached --name-only | awk -F/ '$1=="core" {print $2}' | sort -u)
if [ -n "$NEW_TOOLS" ]; then
  for tool in $NEW_TOOLS; do
    "$PYTHON_EXEC" "$ROOT_DIR/scripts/soft_checkpoints.py" "$tool"
  done
fi

exit 0
"""


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    hooks_dir = root / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_path = hooks_dir / "pre-commit"
    hook_path.write_text(HOOK, encoding="utf-8")
    hook_path.chmod(0o755)
    print("Installed pre-commit hook.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
