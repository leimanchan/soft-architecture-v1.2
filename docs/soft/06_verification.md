# Step 6: Verification

Goal: Ensure boundaries are respected before merge/commit.

## Required Checks
- Run `scripts/check_core_purity.py`
- Run core tests
- Run `scripts/check_test_coverage.py` (staged minimums)
- Run `scripts/check_examples.py`
- Run `scripts/check_adapter_dependencies.py`
- Run `scripts/check_adapter_smoke.py` (Flask adapters)

## Pass Criteria
- Core has no adapter/framework imports
- All decision tests pass
- Coverage meets stage gate:
  - `COVERAGE_STAGE=stage1` -> 65%
  - `COVERAGE_STAGE=stage2` -> 75%
- Adapter dependencies are declared
- Adapter smoke tests return non-5xx responses
