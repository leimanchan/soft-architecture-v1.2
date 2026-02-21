"""Application services / use cases."""

from __future__ import annotations

from typing import Dict, Any


def echo(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"echo": payload}
