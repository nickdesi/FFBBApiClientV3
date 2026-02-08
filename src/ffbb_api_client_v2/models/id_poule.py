from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_str


@dataclass
class IDPoule:
    id: str | None = None
    nom: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> IDPoule:
        assert isinstance(obj, dict)
        id = from_str(obj, "id")
        nom = from_str(obj, "nom")
        return IDPoule(id=id, nom=nom)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.nom is not None:
            result["nom"] = self.nom
        return result
