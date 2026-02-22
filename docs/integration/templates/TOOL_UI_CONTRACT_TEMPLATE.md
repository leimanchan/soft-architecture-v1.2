# UI Contract Template (`adapters/flask/<tool>/UI_CONTRACT.md`)

## Routes

- `GET /`: render tool page
- `POST /<action>`: describe action and expected content type

## Request Payloads

- `<action>`:
  - required fields
  - optional fields
  - validation notes

## Response Shapes

- success payload:
  - keys and types
- error payload:
  - keys and types
  - HTTP status mapping

## UI States

- `idle`: initial view
- `loading`: spinner/progress rules
- `error`: where error text appears
- `success`: what transitions or downloads happen

## Core Contract Binding

- contract entrypoint: `core/<tool>/contracts.py::run`
- mapping location: `adapters/flask/<tool>/presenter.py`
- side effects location: `adapters/flask/<tool>/io.py`

## Notes

- Document any intentional Flask-only behavior.
- Document assumptions that another adapter must preserve.
