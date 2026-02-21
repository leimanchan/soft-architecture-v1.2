#!/usr/bin/env python3
"""Run minimal smoke tests for Flask adapters."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    if not spec or not spec.loader:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _get_app(module):
    if hasattr(module, "create_app"):
        return module.create_app()
    if hasattr(module, "app"):
        return module.app
    return None


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    flask_dir = root / "adapters" / "flask"
    if not flask_dir.exists():
        print("No Flask adapters found.")
        return 0

    tool_dirs = [
        d
        for d in flask_dir.iterdir()
        if d.is_dir() and d.name not in {"_base", "static", "templates"} and not d.name.startswith(".")
    ]
    if not tool_dirs:
        print("No Flask tool adapters found.")
        return 0

    try:
        from flask import Flask
    except Exception:
        print("Flask not available for adapter smoke tests.")
        return 1

    failures: list[str] = []
    for tool_dir in tool_dirs:
        app_path = tool_dir / "app.py"
        if not app_path.exists():
            continue
        module = _load_module(app_path)
        if module is None:
            failures.append(f"{tool_dir.name}: failed to import app.py")
            continue
        app = _get_app(module)
        if not isinstance(app, Flask):
            failures.append(f"{tool_dir.name}: create_app/app not found or not Flask")
            continue
        client = app.test_client()
        routes = {rule.rule: rule for rule in app.url_map.iter_rules()}
        if "/" in routes:
            resp = client.get("/")
            if resp.status_code >= 500:
                failures.append(f"{tool_dir.name}: GET / returned {resp.status_code}")
        for path in ["/generate", "/run"]:
            if path in routes:
                resp = client.post(path, json={})
                if resp.status_code >= 500:
                    failures.append(f"{tool_dir.name}: POST {path} returned {resp.status_code}")

    if failures:
        print("Adapter smoke check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Adapter smoke check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
