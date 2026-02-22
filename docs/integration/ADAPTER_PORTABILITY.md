# Adapter Portability Standard (Flask-First)

Purpose: keep Flask as the default rapid-prototyping adapter while making future adapters (Svelte/Next/etc.) quick to build with LLM agents.

## Principles

- Core contracts are the product boundary (`core/<tool>/contracts.py`).
- Flask is the default runtime adapter and visual baseline.
- Adapter code is translation/presentation only, never business decisions.
- Portability is achieved through explicit artifacts, not framework abstraction layers.

## Required Portability Artifacts

For each tool:

- `core/<tool>/examples/happy_path.json`
- `core/<tool>/examples/invalid_path.json`
- Optional but recommended edge cases:
  - `core/<tool>/examples/edge_cases.json`
- `core/<tool>/application/FILE_MAP.md`
- `adapters/flask/<tool>/UI_CONTRACT.md`:
  - routes/endpoints
  - request/response payloads
  - error payloads/statuses
  - UI states (`idle`, `loading`, `error`, `success`)

## Adapter Boundary Test Minimum

Each Flask adapter should include smoke + boundary tests:

- smoke:
  - index route responds
  - invalid payload path returns expected error shape
- boundary mapping:
  - presenter parses request into contract-compatible payload
  - presenter output mapping preserves contract result shape
  - no business decisions in adapter tests (validate mapping only)

## Review Gates

Before marking a tool complete:

- Can another adapter call the same `contracts.run(...)` without core changes?
- Are UI states/routes documented in `UI_CONTRACT.md`?
- Are adapter boundary tests present for mapping logic?
- Is Flask-specific code isolated to adapter files only?

## Default Position

- Use Flask first unless the user requests otherwise.
- Do not pre-build additional adapters.
- Maintain portability artifacts so alternative adapters can be generated quickly on demand.
