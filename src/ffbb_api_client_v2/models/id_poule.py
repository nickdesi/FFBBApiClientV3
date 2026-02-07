from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_str


class IDPoule:
    id: str | None = None
    nom: str | None = None

    def __init__(self, id: str | None, nom: str | None = None) -> None:
        self.id = id
        self.nom = nom

    @staticmethod
    def from_dict(obj: Any) -> IDPoule:
        assert isinstance(obj, dict)
        id = from_str(obj, "id")
        nom = from_str(obj, "nom")
        return IDPoule(id, nom)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.nom is not None:
            result["nom"] = self.nom
        return result
