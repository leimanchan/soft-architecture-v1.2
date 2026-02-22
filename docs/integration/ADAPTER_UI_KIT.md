# Adapter UI Kit (Flask)

This repo includes a canonical UI kit for Flask adapters.

Location:
- `adapters/flask/_base/`

Contents:
- `templates/base.html`
- `templates/partials/upload_single.html`
- `templates/partials/upload_dual.html`
- `templates/shared_footer.html`
- `templates/demo.html`
- `footer_blueprint.py`
- `static/shared/style.css`
- `static/shared/footer_inject.js`

Rules:
- New Flask tools should extend `base.html` from this kit or copy it verbatim.
- Do not add `<style>` blocks in tool templates. Put custom CSS in a tool-specific file under `static/<tool>/...`.
- Inline `<style>` blocks are allowed only with the marker: `<!-- inline-style:tool-specific -->`.
- Always include `/static/shared/style.css`.
- Register the shared footer blueprint in your Flask app.
- Use `templates/demo.html` as the visual reference. Update the base template/styles to change the look globally.
- Inline styling is a last resort only for hyper tool-specific needs.

This kit is the single source of truth for shared styling.

## Theming Contract

- Prefer shared base classes for common UI (`.btn`, status blocks, upload areas, form controls).
- Customize visuals with CSS variables (tokens) in the tool root container first, instead of redefining shared classes.
- Use tool-scoped overrides only for unique widgets/behaviors that do not fit shared components.
- Avoid generic global selectors in tool CSS (for example bare `.upload-icon`), because they can collide with shared styles.
