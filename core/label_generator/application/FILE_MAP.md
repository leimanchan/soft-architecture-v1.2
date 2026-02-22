# Application File Map

- `input_validation.py`: payload validation/normalization into `LabelJob` (`build_job`)
- `planning.py`: row filtering, slot assignment, and render-plan construction (`compute_plan`)
- `output_format.py`: filename/token formatting and result serialization (`to_result_dict`)
- `service.py`: compatibility facade and re-exports only (`__all__`)
- `orchestrator.py`: dumb sequence of build -> plan -> serialize (`run`)
