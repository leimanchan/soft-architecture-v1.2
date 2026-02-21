#!/usr/bin/env python3
"""Run all preflight checks (core + local)."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CHECKS = [
    "scripts/preflight_core.py",
    "scripts/preflight_local.py",
]


def _python_cmd(root: Path, env: dict[str, str]) -> list[str]:
    override = env.get("PYTHON_EXECUTABLE")
    if override:
        return [override]
    venv_python = root / ".venv" / "bin" / "python"
    if venv_python.exists():
        return [str(venv_python)]
    return ["python3"]


def _write_report(
    report_path: Path,
    checks: list[dict[str, object]],
    python_cmd: list[str],
) -> None:
    failed = [check["check"] for check in checks if check["status"] != "passed"]
    payload = {
        "tool": "preflight",
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
    core_report_path: Path | None = None
    if args.report_json:
        report = Path(args.report_json)
        core_report_path = report.with_name(f"{report.stem}.core{report.suffix}")

    for check in CHECKS:
        path = root / check
        if not path.exists():
            print(f"Missing check: {check}")
            return 1
        cmd = python_cmd + [str(path)]
        if check == "scripts/preflight_core.py":
            if args.full_report:
                cmd.append("--full-report")
            if core_report_path:
                cmd.extend(["--report-json", str(core_report_path)])

        result = subprocess.run(
            cmd,
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)

        check_results.append(
            {
                "check": check,
                "path": str(path),
                "status": "passed" if result.returncode == 0 else "failed",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
        if result.returncode != 0 and stop_on_fail:
            if args.report_json:
                _write_report(Path(args.report_json), check_results, python_cmd)
            return result.returncode

    if args.report_json:
        _write_report(Path(args.report_json), check_results, python_cmd)

    failed_checks = [check for check in check_results if check["status"] != "passed"]
    if failed_checks:
        return int(failed_checks[0]["returncode"])

    print("Preflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
