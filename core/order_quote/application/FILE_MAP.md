# Application File Map

- `input_validation.py`: normalize/validate quote request payload (`build_request`)
- `quote_calculation.py`: pricing, discounts, shipping, and tax decisions (`build_breakdown`)
- `output_mapping.py`: contract output serialization (`to_result_dict`)
- `service.py`: compatibility facade and re-exports only (`__all__`)
- `orchestrator.py`: dumb sequence of request -> breakdown -> output (`run`)
