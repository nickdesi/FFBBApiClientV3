from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_float


class Geo:
    lat: float | None = None
    lng: float | None = None

    def __init__(self, lat: float | None, lng: float | None):
        self.lat = lat
        self.lng = lng

    @staticmethod
    def from_dict(obj: Any) -> Geo:
        assert isinstance(obj, dict)
        lat = from_float(obj, "lat")
        lng = from_float(obj, "lng")
        return Geo(lat, lng)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.lat is not None:
            result["lat"] = self.lat
        if self.lng is not None:
            result["lng"] = self.lng
        return result
