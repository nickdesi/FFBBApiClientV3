from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ..utils.converter_utils import from_uuid


@dataclass
class PurpleLogo:
    id: UUID | None = None

    @staticmethod
    def from_dict(obj: Any) -> PurpleLogo:
        assert isinstance(obj, dict)
        id = from_uuid(obj, "id")
        return PurpleLogo(id=id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = str(self.id)
        return result
