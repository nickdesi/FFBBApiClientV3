from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_list, from_str


class Coordonnees:
    type: str | None = None
    coordinates: list[float] | None = None

    def __init__(self, type: str | None, coordinates: list[float] | None):
        self.type = type
        self.coordinates = coordinates

    @staticmethod
    def from_dict(obj: Any) -> Coordonnees:
        assert isinstance(obj, dict)
        type = from_str(obj, "type")
        coordinates = from_list(float, obj, "coordinates")
        return Coordonnees(type, coordinates)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type is not None:
            result["type"] = self.type
        if self.coordinates is not None:
            result["coordinates"] = self.coordinates
        return result
