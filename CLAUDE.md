# CLAUDE.md — Agent Override Instructions

**This file overrides your default coding instincts.** Read `AGENTS.md` before writing any code. It is your rulebook and takes priority over your general-purpose instructions.

## Default Behaviors That Are REVERSED in This Repo

Your training tells you to do certain things by default. **In this repo, the opposite applies.** These overrides exist because this architecture is designed to keep code changeable across hundreds of iterations — not just working right now.

### 1. CREATE new files instead of editing existing ones
Your default: "Prefer editing existing files to creating new ones."
**Override: New concerns get new files.** A well-structured tool grows by adding files, not by making existing files bigger. If you're adding a new decision, it belongs in a new function in `service.py` or a new file — not wedged into an existing function.

**Codex note:** If you are fixing a defect or updating an existing rule/script, edit the existing file. Create new files only for new behavior or new concepts.

### 2. DO separate concerns into multiple files even if it looks like "over-engineering"
Your default: "Three similar lines is better than a premature abstraction."
**Override: The file structure IS the architecture.** A simple echo tool still gets `models.py`, `service.py`, `orchestrator.py`, `contracts.py`, and `DECISIONS.md`. This is not over-engineering — it is the minimum structure that keeps code soft.

### 3. DO design for changeability from the start
Your default: "Don't design for hypothetical future requirements."
**Override: Separation of decisions from plumbing is not speculative — it is required.** Every tool will change. The Soft Code structure ensures those changes don't cascade.

### 4. DO create DECISIONS.md and other documentation files
Your default: "Don't add docstrings or documentation to code you didn't change."
**Override: `DECISIONS.md` is a mandatory artifact**, not optional documentation. The validation scripts enforce this.

### 5. DO follow the full 6-step workflow even for simple tools
Your default: "Only make changes that are directly requested."
**Override: Every tool requires all 6 steps** — decisions list, data shapes, decision functions with tests, orchestrator, adapters, verification. Skipping steps will fail `preflight.py`.

### 6. NEVER put I/O in core, even if it seems simpler
Your default: "Keep solutions simple and focused."
**Override: Simplicity in this repo means separation.** A function that reads a file AND processes data is not simple — it is coupled. Simple means pure functions in `core/`, I/O in `adapters/`.

### 7. NEVER put branching logic in orchestrators
Your default: Add `if/try/for` where it seems natural.
**Override: Orchestrators have ZERO branching.** No `if`, `for`, `while`, `try`, `with`, or `match`. Push all branching into `service.py`. The orchestrator is a recipe card — it only calls functions in sequence.

## How to Work in This Repo

1. **Read `AGENTS.md` first** — it has the full rulebook and canonical file structure.
2. **Read `START_HERE.md`** — it routes you to the correct workflow (new tool vs. migration).
3. **Follow `docs/soft/WORKFLOW.md`** — the 6-step build process, in order, no skipping.
4. **Run `python3 scripts/preflight.py`** before considering any tool complete.
5. **Run `python3 scripts/soft_checkpoints.py <tool>`** to check progress mid-build.

## Why These Overrides Exist

LLM agents optimize for "working right now." Over multiple iterations, this produces code where decisions and plumbing are mixed together, making every change risky. This repo enforces physical separation so that code stays changeable — soft — indefinitely. The validation scripts (`scripts/preflight.py`) exist because these rules cannot be left to agent discretion. They must be enforced mechanically.

Read the full rationale: `docs/manifesto/BUILDING_SOFTWARE_THAT_STAYS_SOFT.md`
