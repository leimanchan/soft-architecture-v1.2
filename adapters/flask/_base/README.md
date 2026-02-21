# Flask Adapter UI Kit

This is the canonical UI kit for Flask adapters.

## Run the Demo
```
python3 adapters/flask/_base/demo_app.py
```
Then open `http://localhost:8000`.

## Files
- `templates/base.html`
- `templates/demo.html`
- `templates/partials/`
- `templates/shared_footer.html`
- `footer_blueprint.py`
- `static/shared/style.css`

## Rules
- Tool templates must `{% extends "base.html" %}`.
- No `<style>` blocks in tool templates.
- Tool-specific CSS goes in `static/<tool>/...` and is linked in `{% block extra_head %}`.
- Register the shared footer blueprint in your Flask app.
