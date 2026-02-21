# New Tool Checklist

- Core logic exists under `core/<tool>/`.
- Domain models are in `core/<tool>/domain/models.py`.
- Constants/specs are in `core/<tool>/domain/specs.py`.
- Application workflows are in `core/<tool>/application/service.py`.
- Core has no imports of Flask, Click, or adapter modules.
- Adapter is under `adapters/flask/<tool>/` and is thin.
- Adapter maps input → domain models.
- Adapter calls application services only.
- UI/template files are isolated to the adapter.
- `scripts/check_core_purity.py` passes.
