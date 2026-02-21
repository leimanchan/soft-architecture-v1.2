# New Tool Checklist

- Core logic exists under `core/<tool>/`.
- Domain models are in `core/<tool>/domain/models.py`.
- Constants/specs are in `core/<tool>/domain/specs.py`.
- Schema checklist exists in `core/<tool>/domain/schema_checklist.md`.
- Examples exist in `core/<tool>/examples/`.
- Application workflows are in `core/<tool>/application/service.py`.
- Core has no imports of Flask, Click, or adapter modules.
- Adapter is under `adapters/flask/<tool>/` and is thin.
- Adapter uses `io.py` for side effects and `presenter.py` for mapping.
- Adapter declares runtime dependencies in `RUNTIME_DEPENDENCIES.md`.
- Adapter maps input → domain models.
- Adapter calls application services only.
- UI/template files are isolated to the adapter.
- `scripts/check_core_purity.py` passes.
