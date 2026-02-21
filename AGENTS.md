# AGENTS.md — Your Rules for Building Tools

**You are an LLM agent. This file is your rulebook.** Every tool you create or migrate in this repo MUST follow the structure, workflow, and constraints below. These rules are enforced by automated checks — violations will be caught.

Start here: `START_HERE.md`

## Your Job

A user will ask you to build a tool (e.g., "build me a label printer" or "migrate my PDF splitter"). Your job is to produce working code that follows the Soft Code architecture. This means:

1. **All business logic goes in `core/`** — pure Python, no I/O, no framework imports.
2. **All I/O and UI goes in `adapters/`** — thin wrappers that call into core.
3. **You follow the 6-step workflow** in `docs/soft/WORKFLOW.md`, in order, without skipping steps.
4. **You run validation** via `scripts/preflight.py` before finishing.

If you do not follow these rules, the code you produce will become rigid and unmaintainable — the exact problem this architecture exists to prevent.

## Canonical Structure

Every tool you build produces this file tree:

```
core/<tool>/
  DECISIONS.md                 <- Step 1: list every business decision
  contracts.py                 <- Step 2: ToolInput, ToolOutput, run()
  __init__.py                  <- Required for consistent imports
  examples/                    <- Step 2: contract payload examples
    happy_path.json
    invalid_path.json
  domain/
    models.py                  <- Step 2: plain dataclasses
    specs.py                   <- Step 2: constants and specifications
    schema_checklist.md        <- Step 2: required keys/types/defaults
  application/
    service.py                 <- Step 3: pure decision functions
    orchestrator.py            <- Step 4: dumb sequencer (max 60 lines)
  tests/                       <- Step 3: unit tests (no I/O)
  MIGRATION_MAP.md             <- Migration only: old -> new mapping
  README.md                    <- Short per-tool run/usage notes (required)

adapters/flask/<tool>/         <- Step 5: built LAST, after core is complete
  __init__.py
  app.py
  io.py                        <- side effects only
  presenter.py                 <- HTTP/template mapping only
  RUNTIME_DEPENDENCIES.md       <- adapter runtime libs + install command
  assets/                      <- required for tool-specific files (PDFs, etc.)
  templates/
  static/
  tests/                       <- adapter smoke tests (required)
```

## Hard Rules

These are non-negotiable. Automated checks enforce them.

| Rule | Enforced By |
|------|-------------|
| Core must NEVER import Flask, FastAPI, Django, Click, Typer, requests, or adapters | `check_core_purity.py` |
| Core must NEVER use open(), os, pathlib, tempfile, subprocess, socket, shutil, or any I/O | `check_core_no_io.py` |
| Orchestrators must be <=60 lines with NO branching (no if/for/while/try/with/match) | `check_orchestrator_dumb.py` |
| Adapters must NOT be modified until core artifacts exist | `check_adapter_after_core.py` |
| Templates must extend `base.html` from the shared UI kit | `check_adapter_uses_base.py` |
| Templates must NOT contain inline `<style>` blocks | `check_adapter_no_inline_styles.py` |
| All registered tools must have tests | `check_core_tests.py` |
| Tool examples must exist and be valid JSON | `check_examples.py` |
| Schema checklist must exist | `check_schema_checklist.py` |
| Migrated tools must include MIGRATION_MAP.md | `check_migration_map.py` |
| Adapter runtime dependencies must be declared | `check_runtime_dependencies.py` |
| Adapter imports must be declared in requirements | `check_adapter_dependencies.py` |
| Adapter smoke tests must pass (Flask) | `check_adapter_smoke.py` |
| Domain models are plain dataclasses — no methods with side effects | Convention |
| Each tool must include __init__.py in core and adapters packages | Convention |
| Adapters must only call core via contracts.run | Convention |
| tools_registry entries must include name, description, status, contracts, origin, path, icon | Convention |

## Workflow

Follow `docs/soft/WORKFLOW.md` in order. The steps are:

1. **Decisions** — Write `core/<tool>/DECISIONS.md`. List every business decision the tool makes (not how, just what), plus a **Non-goals** section.
2. **Data Shapes** — Create `domain/models.py`, `domain/specs.py`, and `contracts.py`. Plain dataclasses only. Include a `contracts_version` string in ToolInput/ToolOutput and document it in `schema_checklist.md`.
3. **Decision Functions** — Implement `application/service.py` and write tests. Pure functions, no I/O.
4. **Orchestrator** — Write `application/orchestrator.py`. A dumb sequencer that calls your service functions in order. Max 60 lines, no branching.
5. **Adapters** — NOW you can touch `adapters/`. Build Flask routes, templates, static files. Convert HTTP requests to domain objects, call core, convert back.
6. **Verification** — Run `scripts/preflight.py`. All checks must pass.

For migrating existing tools, follow `docs/soft/MIGRATION_WORKFLOW.md` instead.

## Key Docs

- `docs/soft/WORKFLOW.md` — The 6-step build process (your primary guide)
- `docs/integration/CHECKLIST.md` — Requirements checklist for new tools
- `docs/agent/INTERFACE_SPEC.md` — How tools expose contracts for other agents
- `docs/integration/ADAPTER_UI_KIT.md` — Shared Flask template kit
- `docs/manifesto/BUILDING_SOFTWARE_THAT_STAYS_SOFT.md` — The full rationale

## Checks

Run these before you consider a tool complete:

```
python3 scripts/preflight.py              # runs ALL checks
python3 scripts/soft_checkpoints.py <tool> # check workflow progress
python3 scripts/install_hooks.py           # install git hooks
```
