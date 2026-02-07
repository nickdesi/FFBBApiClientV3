from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_int


class TypeClass:
    groupement: int | None = None

    def __init__(self, groupement: int | None = None):
        self.groupement = groupement

    @staticmethod
    def from_dict(obj: Any) -> TypeClass:
        assert isinstance(obj, dict)
        groupement = from_int(obj, "Groupement")
        return TypeClass(groupement)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.groupement is not None:
            result["Groupement"] = self.groupement
        return result
