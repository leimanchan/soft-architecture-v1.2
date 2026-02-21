import pytest

from core.sample_tool.contracts import ToolInput, run


def test_run_rejects_non_dict_payload():
    with pytest.raises(ValueError):
        run(ToolInput(payload="not-a-dict"))
