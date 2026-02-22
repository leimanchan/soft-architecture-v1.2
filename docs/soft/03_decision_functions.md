# Step 3: Decision Functions

Goal: Implement pure logic using the domain shapes.

## Output
- Split decision modules in `core/<tool>/application/` (for example: `input_validation.py`, `decision_logic.py`, `output_mapping.py`)
- Optional: `core/<tool>/application/service.py` as a compatibility facade/re-export layer
- Tests in `core/<tool>/tests/`

## Rules
- No IO. No file paths. No framework imports.
- Functions take domain objects and return domain objects or plain data.
- Each decision is a small, testable function.

## Example
- `filter_blank_records(records) -> records`
- `assign_positions(labels, spec) -> positions`
