# Migration Workflow (Existing Tool → Soft Code)

Use this when converting an existing program into the Soft Code structure.

**Most important rule:** adapters are the last step. Do not touch adapters until core artifacts exist.
**Human gate rule:** stop at each checkpoint, tell the human how to review, and wait for approval before continuing.

## Steps
1. Inventory: identify decision logic vs plumbing in the existing code.
   - Human gate: mark `CP1_DECISIONS` in `core/<tool>/HUMAN_CHECKPOINTS.md` as `APPROVED`.
2. Extract decisions: move pure logic into `core/<tool>/application/service.py`.
3. Define data shapes: create `core/<tool>/domain/models.py` and `specs.py`.
   - Human gate: mark `CP2_DATA_SHAPES` as `APPROVED`.
4. Create orchestrator: add `core/<tool>/application/orchestrator.py` (dumb flow).
   - Human gate: mark `CP4_ORCHESTRATOR` as `APPROVED`.
5. Refactor adapters: move IO/framework code under `adapters/<interface>/<tool>/`.
   - Human gate: mark `CP5_ADAPTERS` as `APPROVED`.
6. Add contracts: `core/<tool>/contracts.py`.
7. Add tests: decision logic only.
   - Human gate: run tests and mark `CP3_CORE_TESTS` as `APPROVED`.
8. Add examples: `core/<tool>/examples/happy_path.json` and `invalid_path.json`.
9. Add migration map: `core/<tool>/MIGRATION_MAP.md`.
10. Register tool: update `tools_registry.json` (origin: migrated).

## Output
- Decision logic lives in core
- IO lives in adapters
- Preflight checks pass
