#!/usr/bin/env python3
"""Enforce preflight checks before running runtime entry points."""

from __future__ import annotations

import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def _python_cmd(root: Path) -> list[str]:
    override = os.environ.get("PYTHON_EXECUTABLE")
    if override:
        return [override]
    venv_python = root / ".venv" / "bin" / "python"
    if venv_python.exists():
        return [str(venv_python)]
    return ["python3"]


def _clear_coverage_artifacts(root: Path) -> None:
    """Remove stale coverage sqlite files that can break deterministic gating."""
    for path in [root / ".coverage", *root.glob(".coverage.*")]:
        if path.exists():
            path.unlink()


def _env_truthy(name: str) -> bool:
    value = os.environ.get(name, "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def enforce_preflight(mode: str = "core") -> int:
    root = Path(__file__).resolve().parents[1]
    python_cmd = _python_cmd(root)
    _clear_coverage_artifacts(root)

    report_dir = root / ".reports"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = report_dir / f"preflight-{mode}-{timestamp}.json"

    if mode == "all":
        script = root / "scripts" / "preflight.py"
    else:
        script = root / "scripts" / "preflight_core.py"
    cmd = python_cmd + [str(script), "--report-json", str(report_path)]
    # Fail fast by default; opt into full-report mode when explicitly requested.
    if _env_truthy("RUNTIME_GATE_FULL_REPORT"):
        cmd.append("--full-report")

    print(f"Enforcing preflight gate ({mode}) before runtime start...")
    result = subprocess.run(cmd, cwd=str(root), env=os.environ.copy(), check=False)
    if result.returncode != 0:
        print("")
        print("Runtime start blocked: preflight checks failed.")
        print(f"Review report: {report_path}")
        return result.returncode

    print(f"Preflight gate passed ({mode}).")
    return 0


def main() -> int:
    mode = os.environ.get("RUNTIME_GATE_MODE", "core").strip().lower() or "core"
    if mode not in {"core", "all"}:
        print(f"Invalid RUNTIME_GATE_MODE '{mode}'. Use 'core' or 'all'.")
        return 1
    return enforce_preflight(mode=mode)


if __name__ == "__main__":
    raise SystemExit(main())
