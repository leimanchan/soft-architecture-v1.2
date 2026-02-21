# Soft Code Workflow (Deterministic)

This is the step-by-step, LLM-friendly build flow. Follow in order. Do not skip steps.

**Most important rule:** adapters are the last step. Do not touch adapters until core artifacts exist.

## Steps
1. `01_decision_list.md`
2. `02_data_shapes.md` (include `contracts.py`)
3. `03_decision_functions.md`
4. `04_orchestrator.md`
5. `05_adapters_and_io.md`
6. `06_verification.md`

## Operating Rules
- One file per step. Keep each doc under ~1 page.
- Never implement IO or framework code in core.
- Each step produces concrete artifacts that the next step relies on.
- Preflight checks must pass before moving on.
- After each critical step, stop and request human review; for migrated tools this approval is required and recorded in `core/<tool>/HUMAN_CHECKPOINTS.md`.

## Artifacts by Step
- Step 1: `DECISIONS.md` in tool folder (include **Non-goals**)
- Step 2: `domain/models.py`, `domain/specs.py`, `domain/schema_checklist.md`, `contracts.py` (include `contracts_version`), `examples/*.json` (include `contracts_version` + `payload`), `__init__.py`, `README.md`, `HUMAN_CHECKPOINTS.md`
- Step 3: `application/service.py` + tests
- Step 4: `application/orchestrator.py`
- Step 5: `adapters/<interface>/<tool>/...` + `__init__.py` + `io.py` + `presenter.py` + `RUNTIME_DEPENDENCIES.md` + `assets/` + adapter smoke tests
- Step 6: run `scripts/preflight.py` (includes adapter smoke + dependency checks)

## Human Gates
- After Step 1: mark `CP1_DECISIONS` as `APPROVED` (required for migrated tools, recommended for new tools).
- After Step 2: mark `CP2_DATA_SHAPES` as `APPROVED` (required for migrated tools, recommended for new tools).
- After Step 3: mark `CP3_CORE_TESTS` as `APPROVED` (required for migrated tools, recommended for new tools).
- After Step 4: mark `CP4_ORCHESTRATOR` as `APPROVED` (required for migrated tools, recommended for new tools).
- After Step 5 (if adapter exists): mark `CP5_ADAPTERS` as `APPROVED` (required for migrated tools, recommended for new tools).

## Skeleton Usage
- Create core first: `scripts/new_tool_skeleton.py <tool_name>`
- Add adapters later, manually, after core artifacts + tests exist.
