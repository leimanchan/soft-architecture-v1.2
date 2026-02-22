from core.label_generator.contracts import ToolInput, run


def test_run_builds_plan_and_filename():
    payload = {
        "sheet_name": "Main Sheet",
        "timestamp_utc": "20260221-1400",
        "use_template": True,
        "copies_per_record": 2,
        "rows": [
            {"Name": "Alice", "Team": "Falcons"},
            {"Name": "", "Team": "ShouldFilter"},
            {"Name": "Bob", "Team": "Wolves"},
        ],
        "label_config": {
            "fields": [
                {"column": "Name", "y": 0.3, "prefix": "Hi ", "suffix": "!", "size": 12},
                {"is_static": True, "static_text": "sports card", "is_header": True, "y": 0.1},
            ]
        },
    }
    result = run(ToolInput(payload=payload))
    plan = result.result

    assert result.contracts_version == "1.0"
    assert plan["filtered_rows"] == 2
    assert plan["total_labels"] == 4
    assert plan["download_name"] == "labels_main_sheet_name_template_20260221_1400.pdf"

    first_slot = plan["slots"][0]
    assert first_slot["page_index"] == 0
    assert first_slot["slot_index"] == 0
    assert first_slot["column_index"] == 0
    assert first_slot["row_index"] == 0
    assert first_slot["x_in"] == 0.175
    assert first_slot["y_in"] == 9.5
    assert first_slot["fields"][0]["text"] == "Hi Alice!"
    assert first_slot["fields"][1]["text"] == "SPORTS CARD"



def test_run_uses_top_down_column_fill_order():
    rows = [{"Name": f"N{i}"} for i in range(11)]
    payload = {
        "sheet_name": "Positions",
        "rows": rows,
        "label_config": {"fields": [{"column": "Name", "y": 0.2}]},
    }
    plan = run(ToolInput(payload=payload)).result

    second_column_first_row = plan["slots"][10]
    assert second_column_first_row["column_index"] == 1
    assert second_column_first_row["row_index"] == 0
    assert second_column_first_row["x_in"] == 2.925
    assert second_column_first_row["y_in"] == 9.5
