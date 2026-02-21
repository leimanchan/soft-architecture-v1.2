#!/usr/bin/env python3
"""Verify agent guidance docs exist and README links them."""

from __future__ import annotations

from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    agents = root / "AGENTS.md"
    docs_index = root / "docs" / "DOCS_INDEX.md"
    readme = root / "README.md"

    missing = [p for p in (agents, docs_index, readme) if not p.exists()]
    if missing:
        print("Missing required file(s):")
        for p in missing:
            print(f"- {p}")
        return 1

    readme_text = readme.read_text(encoding="utf-8")
    required_refs = ["AGENTS.md", "docs/DOCS_INDEX.md"]
    missing_refs = [ref for ref in required_refs if ref not in readme_text]
    if missing_refs:
        print("README missing references to:")
        for ref in missing_refs:
            print(f"- {ref}")
        return 1

    print("Agent docs check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
