# Label Generator (Core)

Pure decision layer for migrated Avery 5160 label generation.

## What It Does
- Validates label-generation payloads.
- Normalizes field config.
- Filters rows by first non-static field.
- Expands rows by `copies_per_record`.
- Computes slot coordinates for Avery 5160 pages.
- Builds deterministic output metadata and download filename.

## What It Does Not Do
- No Excel reads.
- No PDF generation.
- No filesystem or HTTP.

## Contract
- Entry point: `core/label_generator/contracts.py:run`
- Input: `ToolInput(payload=...)`
- Output: `ToolOutput(result=...)` containing a render plan.
