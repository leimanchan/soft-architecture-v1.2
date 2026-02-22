# Schema Checklist

## Required Fields
- `payload.sheet_name`: string (non-empty)
- `payload.rows`: list[dict]
- `payload.label_config.fields`: list[object] (non-empty)

## Field Details
- `payload.copies_per_record`: int, default `1`, range `1..100`
- `payload.use_template`: bool, default `false`
- `payload.timestamp_utc`: string token for deterministic filenames, default `19700101-0000`

Each object in `payload.label_config.fields`:
- `y`: number, required, `0 <= y <= 1.0` (inches from top of label)
- `is_static`: bool, default `false`
- For non-static fields (`is_static=false`): `column` is required non-empty string
- `align`: one of `left|center|right`, default `left`
- `font_family`: string, default `Helvetica`
- `font_weight`: one of `Regular|Bold`, default `Regular`
- `size`: number > 0, default `10`
- `letter_spacing`: number, default `0`
- `is_header`: bool, default `false`
- `static_text`: string, default `""`
- `prefix`: string, default `""`
- `suffix`: string, default `""`

## Defaults
- Missing row values resolve to empty text.
- Value `nan` (case-insensitive string) is treated as empty.
- Header fields are uppercased.
