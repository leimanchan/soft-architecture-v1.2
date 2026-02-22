# Application File Map

- `input_validation.py`: payload validation and normalization (`build_input`)
- `decision_logic.py`: pure echo decision (`compute_echo`)
- `output_mapping.py`: map decision output to contract shape (`to_result_dict`)
- `service.py`: compatibility facade and module re-exports (`echo`)
- `orchestrator.py`: dumb sequence of validate -> compute -> map (`run`)
