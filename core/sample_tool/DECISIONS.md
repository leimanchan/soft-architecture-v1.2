# Decisions

## Problem
- Provide a minimal example tool for the soft-architecture workflow.
- Accept a plain dict payload and return an echoed payload.

## Constraints
- No IO or framework imports in core.
- Keep orchestrator dumb and sequential.

## Behavior
- Happy path: return {"echo": payload}.
- Error: payload must be a dict, otherwise raise ValueError.

## Notes
- This tool is intentionally simple and meant for testing the workflow.
