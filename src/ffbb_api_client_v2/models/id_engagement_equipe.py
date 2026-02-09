from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_obj, from_str
from .logo import Logo


@dataclass
class IDEngagementEquipe:
    id: str | None = None
    nom_usuel: str | None = None
    logo: Logo | None = None

    @staticmethod
    def from_dict(obj: Any) -> IDEngagementEquipe:
        assert isinstance(obj, dict)
        id = from_str(obj, "id")
        nom_usuel = from_str(obj, "nomUsuel")
        logo = from_obj(Logo.from_dict, obj, "logo")
        return IDEngagementEquipe(id=id, nom_usuel=nom_usuel, logo=logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.nom_usuel is not None:
            result["nomUsuel"] = self.nom_usuel
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        return result
