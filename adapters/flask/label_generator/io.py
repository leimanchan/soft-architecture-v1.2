"""I/O utilities for label_generator Flask adapter."""

from __future__ import annotations

import os
import tempfile
from typing import Any


ALLOWED_EXTENSIONS = {"xlsx", "xls"}


def make_upload_dir() -> str:
    return tempfile.mkdtemp(prefix="label_generator_")


def is_allowed_excel(filename: str) -> bool:
    if not filename or "." not in filename:
        return False
    return filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _safe_name(raw: str) -> str:
    cleaned = []
    prev_sep = False
    for char in (raw or "").strip():
        is_alnum = ("a" <= char <= "z") or ("A" <= char <= "Z") or ("0" <= char <= "9")
        if is_alnum:
            cleaned.append(char)
            prev_sep = False
            continue
        if char in {" ", "-", "_", "."} and not prev_sep:
            cleaned.append("_")
            prev_sep = True
    value = "".join(cleaned).strip("_")
    return value or "upload"


def save_upload(file_obj: Any, upload_dir: str) -> tuple[str, str]:
    filename = _safe_name(file_obj.filename or "upload")
    filepath = os.path.join(upload_dir, filename)
    file_obj.save(filepath)
    return filename, filepath


def list_sheet_names(filepath: str) -> list[str]:
    import pandas as pd

    excel_file = pd.ExcelFile(filepath)
    return list(excel_file.sheet_names)


def load_sheet(filepath: str, sheet_name: str) -> tuple[list[str], list[dict[str, Any]], int, list[dict[str, Any]]]:
    import pandas as pd

    df = pd.read_excel(filepath, sheet_name=sheet_name)
    df = df.fillna("")
    columns = [str(col) for col in df.columns.tolist()]
    preview = df.head(5).to_dict("records")
    rows = df.to_dict("records")
    return columns, preview, len(df), rows


def _font_name(family: str, weight: str) -> str:
    if family == "Times":
        return "Times-Bold" if weight == "Bold" else "Times-Roman"
    if weight == "Bold":
        return f"{family}-Bold"
    return family


def render_plan_to_pdf(plan: dict[str, Any], output_path: str) -> str:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(output_path, pagesize=letter)
    layout = plan["layout"]
    label_height = float(layout["label_height_in"])
    label_width = float(layout["label_width_in"])
    text_margin = 0.125 * inch

    current_page = 0
    for slot in plan["slots"]:
        if slot["page_index"] != current_page:
            c.showPage()
            current_page = slot["page_index"]

        label_x = float(slot["x_in"]) * inch
        label_y = float(slot["y_in"]) * inch
        width_pts = label_width * inch

        for field in slot["fields"]:
            text = str(field["text"])
            if not text.strip():
                continue

            font_name = _font_name(str(field["font_family"]), str(field["font_weight"]))
            max_size = float(field["max_size_pt"])
            letter_spacing = float(field["letter_spacing"])

            available_width = width_pts - (2 * text_margin)
            font_size = max_size
            text_width = c.stringWidth(text, font_name, font_size)
            while font_size > 4:
                if letter_spacing != 0:
                    text_width = sum(c.stringWidth(ch, font_name, font_size) for ch in text)
                    text_width += letter_spacing * (len(text) - 1)
                else:
                    text_width = c.stringWidth(text, font_name, font_size)
                if text_width <= available_width:
                    break
                font_size -= 0.5

            c.setFont(font_name, font_size)
            y_from_top = float(field["y_in"])
            draw_y = label_y + (label_height - y_from_top) * inch

            align = str(field["align"])
            if align == "center":
                draw_x = label_x + (width_pts - text_width) / 2
            elif align == "right":
                draw_x = label_x + width_pts - text_width - text_margin
            else:
                draw_x = label_x + text_margin

            if field.get("is_header"):
                c.setFillColor(colors.HexColor("#2d5016"))
            else:
                c.setFillColor(colors.black)

            if letter_spacing != 0:
                current_x = draw_x
                for char in text:
                    c.drawString(current_x, draw_y, char)
                    current_x += c.stringWidth(char, font_name, font_size) + letter_spacing
                final_width = current_x - draw_x
            else:
                c.drawString(draw_x, draw_y, text)
                final_width = text_width

            if field.get("is_header"):
                c.setStrokeColor(colors.HexColor("#2d5016"))
                c.setLineWidth(1)
                c.line(draw_x, draw_y - 2, draw_x + final_width, draw_y - 2)

    c.save()
    return output_path


def merge_with_template(labels_pdf_path: str, template_pdf_path: str, output_path: str) -> str:
    import copy

    from pypdf import PdfReader, PdfWriter

    template_reader = PdfReader(template_pdf_path)
    labels_reader = PdfReader(labels_pdf_path)
    writer = PdfWriter()

    for labels_page in labels_reader.pages:
        template_page = copy.deepcopy(template_reader.pages[0])
        template_page.merge_page(labels_page)
        writer.add_page(template_page)

    with open(output_path, "wb") as out_file:
        writer.write(out_file)

    return output_path


def pdf_response(path: str, download_name: str):
    from flask import send_file

    return send_file(
        path,
        as_attachment=True,
        download_name=download_name,
        mimetype="application/pdf",
    )


def health_json(message: str, status: int = 400) -> tuple[dict[str, str], int]:
    return {"error": message}, status
