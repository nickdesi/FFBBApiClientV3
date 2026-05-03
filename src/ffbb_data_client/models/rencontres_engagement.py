from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_str


@dataclass
class Engagement:
    id: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> Engagement:
        assert isinstance(obj, dict)
        id = from_str(obj, "id")
        return Engagement(id=id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        return result
