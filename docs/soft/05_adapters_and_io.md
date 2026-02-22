# Step 5: Adapters and IO

Goal: Build the interface layer and handle all side effects here.

## Output
- `adapters/<interface>/<tool>/...`
- `adapters/<interface>/<tool>/io.py`
- `adapters/<interface>/<tool>/presenter.py`
- `adapters/<interface>/<tool>/RUNTIME_DEPENDENCIES.md`
- `adapters/<interface>/<tool>/UI_CONTRACT.md`

## Rules
- File IO, HTTP, UI, CLI lives here.
- Adapter converts raw input to domain objects.
- Adapter calls core orchestrator and renders outputs.
- Adapters are last. Create them only after core artifacts exist.
- `io.py` is the only place for side effects.
- `presenter.py` maps HTTP/CLI input to domain and formats output.
- Add boundary tests for adapter mapping (`presenter.py`) in addition to smoke tests.
- Document routes/payloads/error/UI states in `UI_CONTRACT.md` for portability.

## Example
- Parse HTTP request → `LabelConfig`
- Call `orchestrator.generate(...)`
- Write PDF and return response
