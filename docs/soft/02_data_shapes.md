# Step 2: Data Shapes

Goal: Define the domain contracts used by decision code.

## Output
- `core/<tool>/domain/models.py`
- `core/<tool>/domain/specs.py`
- `core/<tool>/contracts.py`

## Rules
- Dataclasses only, no IO, no libraries tied to adapters.
- Shapes must represent domain concepts, not framework objects.

## Example Shapes
- `LabelField`, `LabelConfig`, `SheetSpec`
