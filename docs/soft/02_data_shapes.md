# Step 2: Data Shapes

Goal: Define the domain contracts used by decision code.

## Output
- `core/<tool>/domain/models.py`
- `core/<tool>/domain/specs.py`
- `core/<tool>/domain/schema_checklist.md`
- `core/<tool>/contracts.py`
- `core/<tool>/examples/happy_path.json`
- `core/<tool>/examples/invalid_path.json`

## Rules
- Dataclasses only, no IO, no libraries tied to adapters.
- Shapes must represent domain concepts, not framework objects.
- The schema checklist must enumerate required keys, types, and defaults for nested configs.

## Example Shapes
- `LabelField`, `LabelConfig`, `SheetSpec`
