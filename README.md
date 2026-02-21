# Tool Hub Soft — Program Creation & Unification

This repo is the foundation for building or migrating tools into a strict Soft Code structure. All program creation and unification start here.

Think of this as a treasure chest of small, composable tools that can later be linked into larger systems.

## Structure
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
  agent/
scripts/
```

## Goal
- Core logic has **no IO/framework imports**
- Adapters are thin wrappers around core
- UI can be swapped later (Svelte/CLI)

## Integration Docs
- `docs/integration/CHECKLIST.md`
- `docs/integration/ADAPTER_UI_KIT.md`
- `scripts/new_tool_skeleton.py`
- `scripts/check_core_purity.py`

## Tool Creation
- Core first: `scripts/new_tool_skeleton.py <tool_name>`
- Adapter later: `scripts/new_tool_skeleton.py <tool_name> --with-adapter`

## Manifesto
- `docs/manifesto/BUILDING_SOFTWARE_THAT_STAYS_SOFT.md`

## Run the Flask UI Kit Demo
```
python3 adapters/flask/_base/demo_app.py
```
Then open `http://localhost:8000`.

## Soft Workflow
- `docs/soft/WORKFLOW.md`
- `scripts/soft_flow.py`
- `scripts/soft_checkpoints.py`
- `docs/soft/MIGRATION_WORKFLOW.md`
- `scripts/migration_checkpoints.py`

## Preflight
- `scripts/check_core_no_io.py`
- `scripts/check_core_tests.py`
- `scripts/check_adapter_no_inline_styles.py`
- `scripts/check_adapter_uses_base.py`
- `scripts/preflight.py`
- `scripts/check_adapter_after_core.py`
- `scripts/check_orchestrator_dumb.py`
- `scripts/guard_adapters.py`
- `scripts/check_hooks_installed.py`

## Install Hooks
```
python3 scripts/install_hooks.py
```
- `scripts/check_orchestrator_dumb.py`
- `scripts/guard_adapters.py`

## Agent Guidance
- `AGENTS.md`
- `docs/DOCS_INDEX.md`
- `scripts/check_agent_docs.py`

## Tool Registry
- `tools_registry.json`
- `scripts/register_tool.py`
- `scripts/check_tools_registry.py`
- `scripts/list_tools.py`
- `docs/agent/INTERFACE_SPEC.md`
