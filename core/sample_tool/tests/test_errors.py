import pytest

from core.sample_tool.contracts import ToolInput, run


def test_run_rejects_non_dict_payload():
    with pytest.raises(ValueError):
        run(ToolInput(payload="not-a-dict"))


def test_run_rejects_unsupported_contracts_version():
    with pytest.raises(ValueError):
        run(ToolInput(payload={}, contracts_version="9.9"))
