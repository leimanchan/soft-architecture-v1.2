#!/usr/bin/env python3
"""Enforce split-by-responsibility structure in core/*/application."""

from __future__ import annotations

from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    core_dir = root / "core"
    if not core_dir.exists():
        print("core/ not found")
        return 1

    failures: list[str] = []
    for tool_dir in core_dir.iterdir():
        if not tool_dir.is_dir() or tool_dir.name.startswith("_"):
            continue
        app_dir = tool_dir / "application"
        if not app_dir.exists():
            failures.append(f"{tool_dir.name}: missing application/")
            continue

        orchestrator = app_dir / "orchestrator.py"
        if not orchestrator.exists():
            failures.append(f"{tool_dir.name}: missing application/orchestrator.py")

        py_files = [p.name for p in app_dir.glob("*.py") if p.name != "__init__.py"]
        responsibility_files = [
            name for name in py_files if name not in {"orchestrator.py", "service.py"}
        ]
        if len(responsibility_files) < 2:
            failures.append(
                f"{tool_dir.name}: application/ needs >=2 responsibility modules besides orchestrator.py/service.py"
            )

    if failures:
        print("Application split check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Application split check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
