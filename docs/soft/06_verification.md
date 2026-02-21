# Step 6: Verification

Goal: Ensure boundaries are respected before merge/commit.

## Required Checks
- Run `scripts/check_core_purity.py`
- Run core tests
- Run `scripts/check_test_coverage.py` (staged minimums)

## Pass Criteria
- Core has no adapter/framework imports
- All decision tests pass
- Coverage meets stage gate:
  - `COVERAGE_STAGE=stage1` -> 65%
  - `COVERAGE_STAGE=stage2` -> 75%
