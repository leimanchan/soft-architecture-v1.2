# Agent Interface Spec

This spec defines how agents call tools consistently.

## Tool Contract
Each tool exposes a `core/<tool>/contracts.py` with:
- `ToolInput` dataclass
- `ToolOutput` dataclass
- `contracts_version: str` in both dataclasses
- `run(input: ToolInput) -> ToolOutput`

## Agent Call Pattern
Agents should:
1. Read `core/<tool>/DECISIONS.md`
2. Read `core/<tool>/contracts.py`
3. Review `core/<tool>/examples/happy_path.json` and `invalid_path.json`
4. Review adapter UI contract: `adapters/flask/<tool>/UI_CONTRACT.md` (if present)
5. Call the adapter, or call `run()` in core if available

## Flask-First, Adapter-Portable

- Default adapter target is Flask for rapid prototyping.
- Future adapters should reuse the same contract payload/response shapes.
- Core contract compatibility takes precedence over framework-specific conventions.

## Required Registry Entry
Each tool must be registered in `tools_registry.json` with:
- `name`
- `description`
- `status`
- `contracts` (path to contract file)
- `origin` (`new` or `migrated`)
- `path` (tool root under `core/`)
- `icon` (display icon key/string)

## Status Values
- `active`
- `backburner`
- `deprecated`
