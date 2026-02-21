#!/usr/bin/env python3
"""Enforce required core and adapter structure for each tool."""

from __future__ import annotations

from pathlib import Path

FORBIDDEN_MARKERS = {"todo", "tbd", "fixme"}


def _is_weak_readme(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < 3:
        return True
    lower_text = text.lower()
    if "usage" not in lower_text and "run" not in lower_text:
        return True
    return any(marker in lower_text for marker in FORBIDDEN_MARKERS)


def _check_core_tool(tool_dir: Path, failures: list[str]) -> None:
    init_file = tool_dir / "__init__.py"
    if not init_file.exists():
        failures.append(f"{tool_dir.name}: core __init__.py missing")

    readme_file = tool_dir / "README.md"
    if not readme_file.exists():
        failures.append(f"{tool_dir.name}: core README.md missing")
    else:
        text = readme_file.read_text(encoding="utf-8", errors="ignore")
        if _is_weak_readme(text):
            failures.append(f"{tool_dir.name}: core README.md is too short or placeholder")

    checkpoints_file = tool_dir / "HUMAN_CHECKPOINTS.md"
    if not checkpoints_file.exists():
        failures.append(f"{tool_dir.name}: core HUMAN_CHECKPOINTS.md missing")


def _check_adapter_tool(tool_dir: Path, failures: list[str]) -> None:
    required_files = [
        tool_dir / "__init__.py",
        tool_dir / "app.py",
        tool_dir / "io.py",
        tool_dir / "presenter.py",
        tool_dir / "RUNTIME_DEPENDENCIES.md",
    ]
    for path in required_files:
        if not path.exists():
            failures.append(f"{tool_dir}: missing {path.name}")

    required_dirs = [
        tool_dir / "assets",
        tool_dir / "templates",
        tool_dir / "static",
        tool_dir / "tests",
    ]
    for path in required_dirs:
        if not path.exists() or not path.is_dir():
            failures.append(f"{tool_dir}: missing directory {path.name}")

    tests_dir = tool_dir / "tests"
    if tests_dir.exists():
        test_files = list(tests_dir.glob("test_*.py"))
        if not test_files:
            failures.append(f"{tool_dir}: tests/ must include at least one test_*.py")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    failures: list[str] = []

    core_dir = root / "core"
    if not core_dir.exists():
        print("core/ not found")
        return 1

    for tool_dir in core_dir.iterdir():
        if not tool_dir.is_dir() or tool_dir.name.startswith("_"):
            continue
        _check_core_tool(tool_dir, failures)

    adapters_dir = root / "adapters"
    if adapters_dir.exists():
        for interface_dir in adapters_dir.iterdir():
            if not interface_dir.is_dir():
                continue
            for tool_dir in interface_dir.iterdir():
                if (
                    not tool_dir.is_dir()
                    or tool_dir.name in {"_base", "static", "templates"}
                    or tool_dir.name.startswith(".")
                ):
                    continue
                _check_adapter_tool(tool_dir, failures)

    if failures:
        print("Tool structure check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Tool structure check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
