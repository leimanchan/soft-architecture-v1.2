# UI Contract: label_generator (Flask)

## Routes

- `GET /`: render label generator UI
- `POST /upload`: upload spreadsheet file, return session + worksheet names
- `POST /load_sheet`: load selected worksheet preview/columns/row count
- `POST /generate`: generate PDF (optionally merged with template)
- `POST /run`: contract-only execution path (`payload` passthrough)

## Request Payloads

- `POST /upload`:
  - multipart form-data
  - required: `file` (`.xlsx` or `.xls`)

- `POST /load_sheet`:
  - JSON
  - required: `session_id` (str), `sheet_name` (str)

- `POST /generate`:
  - JSON
  - required: `session_id` (str), `sheet_name` (str), `label_config` (dict)
  - optional: `use_template` (bool), `copies_per_record` (int)

- `POST /run`:
  - JSON
  - required: `payload` (dict matching `core/label_generator/contracts.py`)

## Response Shapes

- success:
  - `/upload`: `{ "success": true, "session_id": str, "sheet_names": [str, ...] }`
  - `/load_sheet`: `{ "success": true, "columns": [str, ...], "preview": [row, ...], "total_rows": int }`
  - `/generate`: PDF binary download
  - `/run`: `{ "success": true, "result": { ...contract result... } }`

- error:
  - JSON: `{ "error": str }`
  - status: `400`, `404`, or `500` depending on validation/session/runtime failure

## UI States

- `idle`: upload area visible
- `loading`: spinner shown during upload/sheet load/pdf generation
- `error`: `.status.error` populated with message
- `success`: step transitions to preview/design/download; generation success message shown

## Core Contract Binding

- Core entrypoint: `core/label_generator/contracts.py::run`
- Mapping logic: `adapters/flask/label_generator/presenter.py`
- Side effects: `adapters/flask/label_generator/io.py`

## Portability Notes

- Alternate adapters should preserve payload/error shapes and `contracts.run` binding.
- UI framework can change, but route semantics and state transitions should remain equivalent.
