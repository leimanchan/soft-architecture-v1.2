#!/usr/bin/env python3
"""Shared footer + tools API for Flask adapters."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from flask import Blueprint, jsonify, render_template_string

BASE_DIR = Path(__file__).resolve().parent
FOOTER_TEMPLATE = BASE_DIR / "templates" / "shared_footer.html"
REGISTRY_PATH = BASE_DIR.parents[2] / "tools_registry.json"

footer_bp = Blueprint("footer_bp", __name__)


def _load_registry() -> Dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {"tools": []}
    try:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"tools": []}


@footer_bp.route("/shared/footer")
def shared_footer():
    html = FOOTER_TEMPLATE.read_text(encoding="utf-8")
    return render_template_string(html)


@footer_bp.route("/api/tools")
def tools_api():
    registry = _load_registry()
    tools = []
    for tool in registry.get("tools", []):
        if tool.get("status") == "deprecated":
            continue
        name = tool.get("name")
        if not name:
            continue
        tools.append({
            "name": name.replace("_", " ").title(),
            "path": tool.get("path") or f"/{name}/",
            "icon": tool.get("icon") or "grid",
        })

    return jsonify({"tools": tools})
