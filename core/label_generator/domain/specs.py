"""Domain specs/constants for Avery 5160 planning."""

AVERY_5160 = {
    "page_width_in": 8.5,
    "page_height_in": 11.0,
    "label_width_in": 2.65,
    "label_height_in": 1.0,
    "left_margin_in": 0.175,
    "top_margin_in": 0.5,
    "columns": 3,
    "rows": 10,
    "horizontal_gap_in": 0.1,
    "vertical_gap_in": 0.0,
}

DEFAULT_FONT_FAMILY = "Helvetica"
DEFAULT_FONT_WEIGHT = "Regular"
DEFAULT_FONT_SIZE_PT = 10.0
DEFAULT_ALIGN = "left"
DEFAULT_TIMESTAMP_UTC = "19700101-0000"

ALLOWED_ALIGNS = {"left", "center", "right"}
ALLOWED_FONT_WEIGHTS = {"Regular", "Bold"}

MIN_FONT_SIZE_PT = 4.0
MAX_COPIES_PER_RECORD = 100
