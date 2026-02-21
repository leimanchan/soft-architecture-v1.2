#!/usr/bin/env python3
"""Run the UI kit demo."""

from __future__ import annotations

from pathlib import Path

import sys
from flask import Flask, render_template

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

ROOT_DIR = BASE_DIR.parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

app = Flask(__name__, template_folder=str(TEMPLATES_DIR), static_folder=str(STATIC_DIR))

# Shared footer + tools API
from adapters.flask._base.footer_blueprint import footer_bp
app.register_blueprint(footer_bp)


@app.route("/")
def index():
    return render_template("demo.html")


if __name__ == "__main__":
    print("UI kit demo running at http://localhost:8000")
    app.run(host="0.0.0.0", port=8000, debug=False)
