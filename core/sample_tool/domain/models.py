"""Domain models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class EchoPayload:
    data: Dict[str, Any]
