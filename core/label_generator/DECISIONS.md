# Decisions

## Problem
- Convert worksheet rows + label design config into a deterministic Avery 5160 render plan.
- Keep all business decisions pure so adapters can render to PDF without re-implementing rules.
- Produce stable output metadata (slot coordinates, prepared text, download filename parts).

## Constraints
- Core cannot touch Excel parsing, filesystem, Flask, or PDF APIs.
- Coordinates are computed in inches using a fixed Avery 5160 spec.
- Invalid payload shapes must fail fast with `ValueError`.
- `copies_per_record` is bounded to avoid accidental output explosions.

## Behavior
- Non-static first field decides blank-row filtering.
- Copies are expanded after filtering (`n` rows * `copies_per_record`).
- Static fields always render from `static_text`; data fields resolve from row values.
- Data-field prefixes/suffixes apply only when field value is non-empty.
- Header fields force uppercase text and bold weight.
- Slot fill order is top-down by column (0-9, 10-19, 20-29).
- Download name includes sheet token, first dynamic column token, optional template tag, and timestamp token.

## Non-goals
- No direct PDF drawing, font registration, or text-width measurement.
- No Excel file reading/parsing in core.
- No HTTP/session handling.
- No persistent storage for uploads, presets, or generated artifacts.

## Notes
- Adapter will supply `rows` already loaded from worksheet.
- Adapter is responsible for mapping this render plan into ReportLab + optional template merge.
