"""Flask adapter for migrated label_generator."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request
from jinja2 import ChoiceLoader, FileSystemLoader

ROOT = Path(__file__).resolve().parents[3]


try:
    from adapters.flask._base.footer_blueprint import footer_bp
    from adapters.flask.label_generator import io, presenter
    from core.label_generator.contracts import ToolInput, run as run_contract
except ModuleNotFoundError:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from adapters.flask._base.footer_blueprint import footer_bp
    from adapters.flask.label_generator import io, presenter
    from core.label_generator.contracts import ToolInput, run as run_contract

BASE_TEMPLATES = ROOT / "adapters" / "flask" / "_base" / "templates"
TOOL_TEMPLATES = ROOT / "adapters" / "flask" / "label_generator" / "templates"
BASE_STATIC = ROOT / "adapters" / "flask" / "_base" / "static"
TOOL_STATIC = ROOT / "adapters" / "flask" / "label_generator" / "static"
TOOL_ASSETS = ROOT / "adapters" / "flask" / "label_generator" / "assets"


def create_app() -> Flask:
    app = Flask(__name__, static_folder=str(BASE_STATIC), static_url_path="/static")
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
    app.config["UPLOAD_FOLDER"] = io.make_upload_dir()

    app.jinja_loader = ChoiceLoader(
        [
            FileSystemLoader(str(TOOL_TEMPLATES)),
            FileSystemLoader(str(BASE_TEMPLATES)),
        ]
    )
    app.register_blueprint(footer_bp)

    @app.route("/static/label_generator/<path:filename>")
    def tool_static(filename: str):
        from flask import send_from_directory

        return send_from_directory(str(TOOL_STATIC), filename)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/upload", methods=["POST"])
    def upload_file():
        if "file" not in request.files:
            return jsonify(presenter.error_payload("No file uploaded")), 400

        file_obj = request.files["file"]
        if not file_obj.filename:
            return jsonify(presenter.error_payload("No file selected")), 400

        if not io.is_allowed_excel(file_obj.filename):
            return jsonify(presenter.error_payload("Invalid file type. Please upload .xlsx or .xls")), 400

        try:
            session_id, filepath = io.save_upload(file_obj, app.config["UPLOAD_FOLDER"])
            sheet_names = io.list_sheet_names(filepath)
            return jsonify({"success": True, "session_id": session_id, "sheet_names": sheet_names})
        except Exception as exc:
            return jsonify(presenter.error_payload(f"Error reading Excel file: {exc}")), 500

    @app.route("/load_sheet", methods=["POST"])
    def load_sheet():
        body = request.get_json(silent=True) or {}
        try:
            session_id, sheet_name = presenter.parse_load_sheet_request(body)
        except ValueError:
            return jsonify(presenter.error_payload("Missing required data")), 400

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], session_id)
        if not os.path.exists(filepath):
            return jsonify(presenter.error_payload("Session file not found")), 404

        try:
            columns, preview, total_rows, _rows = io.load_sheet(filepath, sheet_name)
            return jsonify(
                {
                    "success": True,
                    "columns": columns,
                    "preview": preview,
                    "total_rows": total_rows,
                }
            )
        except Exception as exc:
            return jsonify(presenter.error_payload(f"Error loading sheet: {exc}")), 500

    @app.route("/generate", methods=["POST"])
    def generate_labels():
        body = request.get_json(silent=True) or {}
        try:
            session_id, sheet_name, _label_config = presenter.parse_generate_request(body)
        except ValueError:
            return jsonify(presenter.error_payload("Missing required data")), 400

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], session_id)
        if not os.path.exists(filepath):
            return jsonify(presenter.error_payload("Session file not found")), 404

        try:
            _columns, _preview, _total_rows, rows = io.load_sheet(filepath, sheet_name)
            payload = presenter.build_generate_payload(body, rows)
            result = run_contract(ToolInput(payload=payload)).result

            labels_pdf = os.path.join(app.config["UPLOAD_FOLDER"], f"labels_{session_id}.pdf")
            io.render_plan_to_pdf(result, labels_pdf)

            output_path = labels_pdf
            if bool(body.get("use_template", False)):
                template_pdf = TOOL_ASSETS / "Avery5160AddressLabelsOutlineTemplate.pdf"
                merged_pdf = os.path.join(app.config["UPLOAD_FOLDER"], f"labels_with_template_{session_id}.pdf")
                io.merge_with_template(labels_pdf, str(template_pdf), merged_pdf)
                output_path = merged_pdf

            return io.pdf_response(output_path, result["download_name"])
        except ValueError as exc:
            return jsonify(presenter.error_payload(str(exc))), 400
        except Exception as exc:
            return jsonify(presenter.error_payload(f"Error generating labels: {exc}")), 500

    @app.route("/run", methods=["POST"])
    def run_contract_only():
        body: dict[str, Any] = request.get_json(silent=True) or {}
        try:
            payload = presenter.parse_run_request(body)
        except ValueError:
            return jsonify(presenter.error_payload("payload is required")), 400
        try:
            result = run_contract(ToolInput(payload=payload)).result
            return jsonify({"success": True, "result": result})
        except ValueError as exc:
            return jsonify(presenter.error_payload(str(exc))), 400

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
