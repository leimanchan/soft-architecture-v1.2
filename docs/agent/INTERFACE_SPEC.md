# Agent Interface Spec

This spec defines how agents call tools consistently.

## Tool Contract
Each tool exposes a `core/<tool>/contracts.py` with:
- `ToolInput` dataclass
- `ToolOutput` dataclass
- `run(input: ToolInput) -> ToolOutput`

## Agent Call Pattern
Agents should:
1. Read `core/<tool>/DECISIONS.md`
2. Read `core/<tool>/contracts.py`
3. Review `core/<tool>/examples/happy_path.json` and `invalid_path.json`
4. Call the adapter, or call `run()` in core if available

## Required Registry Entry
Each tool must be registered in `tools_registry.json` with:
- `name`
- `description`
- `status`
- `contracts` (path to contract file)

## Status Values
- `active`
- `backburner`
- `deprecated`
