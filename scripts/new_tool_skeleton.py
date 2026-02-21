#!/usr/bin/env python3
"""Create a new tool skeleton following the core + adapter structure."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: scripts/new_tool_skeleton.py <tool_name>")
        return 1

    tool_name = sys.argv[1].strip().lower().replace(" ", "_")
    if not tool_name:
        print("Tool name is required.")
        return 1

    root = Path(__file__).resolve().parents[1]

    core_dir = root / "core" / tool_name
    domain_dir = core_dir / "domain"
    app_dir = core_dir / "application"
    tests_dir = core_dir / "tests"

    flask_dir = root / "adapters" / "flask" / tool_name
    flask_templates = flask_dir / "templates"
    flask_static = flask_dir / "static"

    for d in [domain_dir, app_dir, tests_dir, flask_templates, flask_static]:
        d.mkdir(parents=True, exist_ok=True)

    (core_dir / "__init__.py").touch(exist_ok=True)

    (core_dir / "DECISIONS.md").write_text(
        "# Decisions\n\n- TODO\n",
        encoding="utf-8",
    )

    (domain_dir / "models.py").write_text(
        """\"\"\"Domain models.\"\"\"\n\n""",
        encoding="utf-8",
    )

    (domain_dir / "specs.py").write_text(
        """\"\"\"Domain specs/constants.\"\"\"\n\n""",
        encoding="utf-8",
    )

    (core_dir / "contracts.py").write_text(
        """\"\"\"Tool contract.\"\"\"\n\n""",
        encoding="utf-8",
    )

    (app_dir / "service.py").write_text(
        """\"\"\"Application services / use cases.\"\"\"\n\n""",
        encoding="utf-8",
    )

    (app_dir / "orchestrator.py").write_text(
        """\"\"\"Dumb orchestrator.\"\"\"\n\n""",
        encoding="utf-8",
    )

    (flask_dir / "app.py").write_text(
        """#!/usr/bin/env python3\n\"\"\"Flask adapter.\"\"\"\n\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/')\ndef index():\n    return 'OK'\n\nif __name__ == '__main__':\n    app.run(host='0.0.0.0', port=8000, debug=False)\n""",
        encoding="utf-8",
    )

    # Auto-register tool in tools_registry.json if present
    registry_path = root / "tools_registry.json"
    if registry_path.exists():
        try:
            import json

            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            tools = registry.get("tools", [])
            if not any(tool.get("name") == tool_name for tool in tools):
                tools.append({
                    "name": tool_name,
                    "description": "TODO",
                    "status": "active",
                    "contracts": f"core/{tool_name}/contracts.py",
                })
                registry["tools"] = tools
                registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
        except Exception:
            pass

    print(f"Created skeleton for: {tool_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
