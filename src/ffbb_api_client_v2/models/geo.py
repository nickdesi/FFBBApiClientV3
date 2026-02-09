from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_float


@dataclass
class Geo:
    lat: float | None = None
    lng: float | None = None

    @staticmethod
    def from_dict(obj: Any) -> Geo:
        assert isinstance(obj, dict)
        lat = from_float(obj, "lat")
        lng = from_float(obj, "lng")
        return Geo(lat=lat, lng=lng)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.lat is not None:
            result["lat"] = self.lat
        if self.lng is not None:
            result["lng"] = self.lng
        return result
