# Migration Map: `tool-hub-unified/tools/label_generator` -> `core/label_generator`

## Source Inventory
- Source app: `/Users/leimanchan/Documents/tool-hub-unified/tools/label_generator/app.py`
- Interface: Flask routes (`/upload`, `/load_sheet`, `/generate`)
- IO dependencies: `pandas`, `reportlab`, `pypdf`, filesystem temp uploads

## Extracted to Core
- Filename planning:
  - source `build_download_name(...)`
  - migrated to `core/label_generator/application/service.py:_download_name(...)`
- Data filtering rule:
  - source filters blank rows by first non-static field
  - migrated to `service._filter_rows(...)`
- Copies expansion rule:
  - source duplicates rows by `copies_per_record`
  - migrated to `service._expand_rows(...)`
- Avery slot positioning:
  - source `get_label_position(index)`
  - migrated to `service._slot_coordinates(slot_index)`
- Text resolution decisions:
  - static vs dynamic text, `nan` handling, prefix/suffix, header uppercase
  - migrated to `service._resolve_text(...)`

## Remaining in Adapter (Not Yet Migrated)
- Excel upload and worksheet reads (`pandas`)
- PDF drawing, font measurement/shrink loops, header underline rendering (`reportlab`)
- Optional template merge (`pypdf`)
- Flask request/response/session/file-path plumbing

## Contract Boundary
- Core input: normalized payload with `rows` and `label_config`
- Core output: deterministic render plan (`slots`, `fields`, coordinates, metadata)
- Adapter responsibility: transform HTTP + worksheet IO into `ToolInput.payload`, then consume `ToolOutput.result`
