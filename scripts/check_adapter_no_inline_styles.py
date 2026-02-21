#!/usr/bin/env python3
"""Fail if adapter templates include inline <style> blocks without marker."""

from __future__ import annotations

from pathlib import Path

MARKER = "inline-style:tool-specific"


def _style_blocks(text: str) -> list[int]:
    offsets = []
    idx = 0
    while True:
        idx = text.find("<style", idx)
        if idx == -1:
            break
        offsets.append(idx)
        idx += 6
    return offsets


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    templates_root = root / "adapters" / "flask"
    if not templates_root.exists():
        print("adapters/flask not found")
        return 0

    violations = []
    for path in templates_root.rglob("*.html"):
        if "_base" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        offsets = _style_blocks(text)
        if not offsets:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if "<style" in line:
                window = "\n".join(lines[max(i-2, 0):i+1])
                if MARKER not in window:
                    violations.append(f"{path}:{i+1}")

    if violations:
        print("Inline <style> blocks found without marker:")
        for v in violations:
            print(f"- {v}")
        return 1

    print("Adapter inline style check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
