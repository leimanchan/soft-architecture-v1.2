# Step 4: Dumb Orchestrator

Goal: Wire decisions together in a simple recipe.

## Output
- `core/<tool>/application/orchestrator.py`

## Rules
- No conditional business logic.
- Only sequencing calls to decision functions.
- No IO.

## Example
```
records = filter_blank_records(records)
labels = build_labels(records)
positions = assign_positions(labels, spec)
return positions
```
