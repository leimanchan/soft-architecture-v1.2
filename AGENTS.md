# AGENTS.md

This repo is the mandatory starting point for creating or migrating any tool. All program creation and future unification start here.

This repo uses a strict Soft Code workflow to keep business logic decoupled from interfaces.

## Canonical Structure
```
core/
  <tool>/
    DECISIONS.md
    domain/
      models.py
      specs.py
    application/
      service.py
      orchestrator.py
    tests/
adapters/
  flask/
    <tool>/
      app.py
      templates/
      static/
docs/
  soft/
  integration/
scripts/
```

## Hard Rules
- Core must never import Flask/CLI/UI libraries.
- All IO and frameworks live in adapters.
- Domain models are plain data shapes.
- Application layer wires decisions together (no IO).
- Orchestrator is dumb and sequential.
- Adapters are the last step. Do not modify adapters until core artifacts exist.
- Adapter templates must extend the base kit and never use inline `<style>` blocks. Inline styling is a last resort only for hyper tool-specific needs and must include `<!-- inline-style:tool-specific -->`.

## Soft Code Workflow
Follow `docs/soft/WORKFLOW.md` in order.

## Two Paths
- New tool: follow `docs/soft/WORKFLOW.md`.
- Existing tool migration: follow `docs/soft/MIGRATION_WORKFLOW.md`.

## Key Docs
- `docs/soft/WORKFLOW.md`
- `docs/integration/CHECKLIST.md`
- `docs/agent/INTERFACE_SPEC.md`
- `docs/integration/ADAPTER_UI_KIT.md`
- `docs/manifesto/BUILDING_SOFTWARE_THAT_STAYS_SOFT.md`

## Checks
- `scripts/check_core_purity.py`
- `scripts/soft_checkpoints.py <tool_name>`
- `scripts/preflight.py`
