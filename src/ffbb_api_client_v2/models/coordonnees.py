from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_list, from_str


@dataclass
class Coordonnees:
    type: str | None = None
    coordinates: list[float] | None = None

    @staticmethod
    def from_dict(obj: Any) -> Coordonnees:
        assert isinstance(obj, dict)
        type = from_str(obj, "type")
        coordinates = from_list(float, obj, "coordinates")
        return Coordonnees(type=type, coordinates=coordinates)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = self.type
        if self.coordinates is not None:
            result["coordinates"] = self.coordinates
        return result
