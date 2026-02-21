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

## Artifacts by Step
- Step 1: `DECISIONS.md` in tool folder
- Step 2: `domain/models.py`, `domain/specs.py`, `contracts.py`
- Step 3: `application/service.py` + tests
- Step 4: `application/orchestrator.py`
- Step 5: `adapters/<interface>/<tool>/...`
- Step 6: run `scripts/check_core_purity.py` + tests
