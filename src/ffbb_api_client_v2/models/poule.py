from __future__ import annotations

from typing import Any

from ..utils.converter_utils import (
    from_list,
    from_str,
)
from .multi_search_result_rencontres import Engagement


class Poule:
    nom: str | None = None
    id: str | None = None
    engagements: list[Engagement] | None = None

    def __init__(
        self,
        nom: str | None,
        id: str | None,
        engagements: list[Engagement] | None,
    ):
        self.nom = nom
        self.id = id
        self.engagements = engagements

    @staticmethod
    def from_dict(obj: Any) -> Poule:
        assert isinstance(obj, dict)
        nom = from_str(obj, "nom")
        id = from_str(obj, "id")
        engagements = from_list(Engagement.from_dict, obj, "engagements")
        return Poule(nom, id, engagements)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = self.nom
        if self.id is not None:
            result["id"] = self.id
        if self.engagements is not None:
            result["engagements"] = [e.to_dict() for e in self.engagements]
        return result
