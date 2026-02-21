#!/usr/bin/env python3
"""Run core repository checks (CI-safe)."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CHECKS = [
    "scripts/check_protected_files.py",
    "scripts/check_core_purity.py",
    "scripts/check_core_no_io.py",
    "scripts/check_decisions_quality.py",
    "scripts/check_schema_checklist.py",
    "scripts/check_examples.py",
    "scripts/check_core_tests.py",
    "scripts/check_contracts.py",
    "scripts/check_test_coverage.py",
    "scripts/check_agent_docs.py",
    "scripts/check_tools_registry.py",
    "scripts/check_migration_map.py",
    "scripts/check_runtime_dependencies.py",
    "scripts/check_adapter_dependencies.py",
    "scripts/check_adapter_smoke.py",
    "scripts/check_adapter_no_inline_styles.py",
    "scripts/check_adapter_uses_base.py",
    "scripts/check_adapter_sequence.py",
    "scripts/check_orchestrator_dumb.py",
]


def _python_cmd(root: Path, env: dict[str, str]) -> list[str]:
    override = env.get("PYTHON_EXECUTABLE")
    if override:
        return [override]
    venv_python = root / ".venv" / "bin" / "python"
    if venv_python.exists():
        return [str(venv_python)]
    return ["python3"]


def _run_one_check(
    root: Path,
    env: dict[str, str],
    python_cmd: list[str],
    check: str,
) -> dict[str, object]:
    path = root / check
    if not path.exists():
        print(f"Missing check: {check}")
        return {
            "check": check,
            "path": str(path),
            "status": "missing",
            "returncode": 1,
            "stdout": "",
            "stderr": "",
        }

    result = subprocess.run(
        python_cmd + [str(path)],
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return {
        "check": check,
        "path": str(path),
        "status": "passed" if result.returncode == 0 else "failed",
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def _write_report(
    report_path: Path,
    checks: list[dict[str, object]],
    python_cmd: list[str],
) -> None:
    failed = [check["check"] for check in checks if check["status"] != "passed"]
    payload = {
        "tool": "preflight_core",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total": len(checks),
            "passed": sum(1 for check in checks if check["status"] == "passed"),
            "failed": len(failed),
            "failed_checks": failed,
        },
        "python_cmd": python_cmd,
        "checks": checks,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote preflight report: {report_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report-json",
        help="Write structured check results to this JSON file.",
    )
    parser.add_argument(
        "--full-report",
        action="store_true",
        help="Run all checks and report every failure (default stops at first failure).",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    python_cmd = _python_cmd(root, env)
    stop_on_fail = not args.full_report
    check_results: list[dict[str, object]] = []

    for check in CHECKS:
        check_result = _run_one_check(root, env, python_cmd, check)
        check_results.append(check_result)
        if check_result["status"] != "passed" and stop_on_fail:
            if args.report_json:
                _write_report(Path(args.report_json), check_results, python_cmd)
            return int(check_result["returncode"])

    if args.report_json:
        _write_report(Path(args.report_json), check_results, python_cmd)

    failed_checks = [check for check in check_results if check["status"] != "passed"]
    if failed_checks:
        return int(failed_checks[0]["returncode"])

    print("Preflight core passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
