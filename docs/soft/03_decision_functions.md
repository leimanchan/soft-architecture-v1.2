# Step 3: Decision Functions

Goal: Implement pure logic using the domain shapes.

## Output
- `core/<tool>/application/service.py`
- Tests in `core/<tool>/tests/`

## Rules
- No IO. No file paths. No framework imports.
- Functions take domain objects and return domain objects or plain data.
- Each decision is a small, testable function.

## Example
- `filter_blank_records(records) -> records`
- `assign_positions(labels, spec) -> positions`
