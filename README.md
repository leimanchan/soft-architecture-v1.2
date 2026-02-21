# Tool Hub Soft — Agent Instruction Set for Building Soft Code

**This repo is not an application. You do not run it.** It is an instruction set and enforcement framework for LLM agents. When a user asks you to build or migrate a tool, this repo tells you exactly how — what files to create, what rules to follow, what checks to pass.

Start here: `START_HERE.md`

Read `AGENTS.md` first. That is your rulebook.

## What This Repo Contains

| What | Purpose |
|------|---------|
| `AGENTS.md` | **Start here.** Your hard rules and constraints. |
| `docs/soft/WORKFLOW.md` | The 6-step deterministic build process you must follow. |
| `docs/manifesto/` | The "why" — why soft code matters and what goes wrong without it. |
| `scripts/` | Validation checks and scaffolding tools you run during the build. |
| `core/` | Where you place the pure business logic for each tool you build. |
| `adapters/` | Where you place interface code (Flask, CLI, etc.) — always last. |
| `tools_registry.json` | Central registry of all tools you have built. |

## How You Use This Repo (Agent Workflow)

When a user says "build me a tool that does X":

1. **Read your rules** — open `AGENTS.md` and internalize the hard rules.
2. **Scaffold** — run `scripts/new_tool_skeleton.py <tool_name>` to create the directory structure.
3. **Follow the workflow** — work through `docs/soft/WORKFLOW.md` steps 1–6 in order. Each step produces concrete files that the next step depends on.
4. **Validate** — run `scripts/preflight.py` before committing. All checks must pass.
5. **Register** — the tool must appear in `tools_registry.json` with status, description, and contract path.

When a user says "migrate an existing tool":

1. Follow `docs/soft/MIGRATION_WORKFLOW.md` instead of the new-tool workflow.
2. Same rules apply — core first, adapters last, all checks must pass.

## The One Rule That Matters

**Decisions live in `core/`. Plumbing lives in `adapters/`.** Never mix them. Core has zero I/O, zero framework imports. Adapters are thin wrappers that convert external formats to domain objects and back. This separation is enforced by automated checks — you cannot skip it.

## Directory Structure

```
core/                          <- Pure logic. No I/O. No frameworks.
  <tool>/
    DECISIONS.md               <- What this tool decides (not how)
    contracts.py               <- ToolInput, ToolOutput, run()
    domain/
      models.py                <- Plain dataclasses
      specs.py                 <- Constants and specifications
    application/
      service.py               <- Pure decision functions
      orchestrator.py          <- Dumb sequencer (max 60 lines, no branching)
    tests/                     <- Unit tests (no I/O needed)

adapters/                      <- I/O and frameworks live here.
  flask/
    _base/                     <- Shared UI kit (templates, styles, footer)
    <tool>/
      app.py                   <- Flask routes
      templates/               <- HTML (must extend base.html)
      static/                  <- CSS (no inline styles)

scripts/                       <- Validation and scaffolding.
  preflight.py                 <- Master check (runs all validators)
  new_tool_skeleton.py         <- Scaffold a new tool
  soft_checkpoints.py          <- Check workflow progress
  check_core_purity.py         <- No framework imports in core
  check_core_no_io.py          <- No I/O in core
  check_orchestrator_dumb.py   <- Orchestrator <=60 lines, no branching
  ...

docs/                          <- Workflow docs, manifesto, integration guides.
```

## Key References

- **Rules**: `AGENTS.md`
- **Build workflow**: `docs/soft/WORKFLOW.md` (steps 1–6)
- **Migration workflow**: `docs/soft/MIGRATION_WORKFLOW.md`
- **Manifesto**: `docs/manifesto/BUILDING_SOFTWARE_THAT_STAYS_SOFT.md`
- **Integration checklist**: `docs/integration/CHECKLIST.md`
- **UI kit**: `docs/integration/ADAPTER_UI_KIT.md`
- **Agent calling conventions**: `docs/agent/INTERFACE_SPEC.md`
- **All docs**: `docs/DOCS_INDEX.md`

## Install Hooks
```
python3 scripts/install_hooks.py
```

## Preflight
```
python3 scripts/preflight.py
```

## CI vs Local
- CI: `python3 scripts/preflight_core.py`
- Local: `python3 scripts/preflight.py`

## Flask UI Kit Demo

To preview the shared UI components (not a tool — just the base template kit):
```
python3 adapters/flask/_base/demo_app.py
```
Then open `http://localhost:8000`.
