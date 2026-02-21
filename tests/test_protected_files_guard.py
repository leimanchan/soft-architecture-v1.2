from scripts.check_protected_files import (
    _is_override_allowed,
    _matches_protected,
    _override_patterns,
)


def test_matches_protected_patterns():
    assert _matches_protected("tests/test_enforcement_flow.py")
    assert _matches_protected("scripts/check_core_purity.py")
    assert _matches_protected("scripts/preflight_core.py")
    assert _matches_protected(".github/workflows/preflight.yml")


def test_non_protected_paths():
    assert not _matches_protected("core/sample_tool/contracts.py")
    assert not _matches_protected("docs/soft/WORKFLOW.md")
    assert not _matches_protected("scripts/new_tool_skeleton.py")


def test_override_patterns_parsing(monkeypatch):
    monkeypatch.setenv("ALLOW_PROTECTED_CHANGES", "scripts/check_core_tests.py,scripts/preflight.py")
    assert _override_patterns() == ["scripts/check_core_tests.py", "scripts/preflight.py"]


def test_override_pattern_global(monkeypatch):
    monkeypatch.setenv("ALLOW_PROTECTED_CHANGES", "1")
    assert _override_patterns() == ["*"]


def test_override_allowed_scoped():
    patterns = ["scripts/check_core_tests.py", "scripts/preflight*.py"]
    assert _is_override_allowed("scripts/check_core_tests.py", patterns)
    assert _is_override_allowed("scripts/preflight_core.py", patterns)
    assert not _is_override_allowed(".github/workflows/preflight.yml", patterns)
