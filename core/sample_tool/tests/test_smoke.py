from core.sample_tool.contracts import ToolInput, run


def test_run_returns_distinct_result_object():
    payload = {"k": "v"}
    output = run(ToolInput(payload=payload))
    assert output.result == {"echo": payload}
    assert output.result is not payload
