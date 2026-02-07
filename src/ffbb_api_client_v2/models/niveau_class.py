from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_int


class NiveauClass:
    départemental: int | None = None
    régional: int | None = None

    def __init__(self, départemental: int | None, régional: int | None) -> None:
        self.départemental = départemental
        self.régional = régional

    @staticmethod
    def from_dict(obj: Any) -> NiveauClass:
        assert isinstance(obj, dict)
        départemental = from_int(obj, "Départemental")
        régional = from_int(obj, "Régional")
        return NiveauClass(départemental, régional)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.départemental is not None:
            result["Départemental"] = self.départemental
        if self.régional is not None:
            result["Régional"] = self.régional
        return result
