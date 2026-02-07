from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_obj, from_str
from .logo import Logo


class TypeCompetitionGenerique:
    type_competition_generique_id: str | None = None
    logo: Logo | None = None

    def __init__(self, id: str | None, logo: Logo | None) -> None:
        self.type_competition_generique_id = id
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> TypeCompetitionGenerique:
        assert isinstance(obj, dict)
        type_competition_generique_id = from_str(obj, "id")
        logo = from_obj(Logo.from_dict, obj, "logo")
        return TypeCompetitionGenerique(type_competition_generique_id, logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.type_competition_generique_id is not None:
            result["id"] = self.type_competition_generique_id
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        return result
