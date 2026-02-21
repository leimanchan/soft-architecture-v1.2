#!/usr/bin/env python3
"""Fail if adapter templates include inline <style> blocks."""

from __future__ import annotations

from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    templates_root = root / "adapters" / "flask"
    if not templates_root.exists():
        print("adapters/flask not found")
        return 0

    violations = []
    for path in templates_root.rglob("*.html"):
        # Skip the base kit itself
        if "_base" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "<style" in text:
            if "inline-style:tool-specific" not in text:
                violations.append(str(path))

    if violations:
        print("Inline <style> blocks found in templates:")
        for v in violations:
            print(f"- {v}")
        return 1

    print("Adapter inline style check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
