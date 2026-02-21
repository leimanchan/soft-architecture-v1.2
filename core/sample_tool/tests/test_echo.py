from core.sample_tool.contracts import ToolInput, run


def test_run_echo():
    payload = {"hello": "world"}
    result = run(ToolInput(payload=payload))
    assert result.result == {"echo": payload}
