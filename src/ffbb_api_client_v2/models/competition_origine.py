from __future__ import annotations

from typing import Any

from ..utils.converter_utils import (
    from_obj,
    from_str,
)
from .competition_origine_categorie import CompetitionOrigineCategorie
from .competition_origine_type_competition import CompetitionOrigineTypeCompetition
from .competition_origine_type_competition_generique import (
    CompetitionOrigineTypeCompetitionGenerique,
)


class CompetitionOrigine:
    id: str | None = None
    code: str | None = None
    nom: str | None = None
    type_competition: CompetitionOrigineTypeCompetition | None = None
    categorie: CompetitionOrigineCategorie | None = None
    type_competition_generique: CompetitionOrigineTypeCompetitionGenerique | None = None

    def __init__(
        self,
        id: str | None,
        code: str | None,
        nom: str | None,
        type_competition: CompetitionOrigineTypeCompetition | None,
        categorie: CompetitionOrigineCategorie | None,
        type_competition_generique: None | (CompetitionOrigineTypeCompetitionGenerique),
    ) -> None:
        self.id = id
        self.code = code
        self.nom = nom
        self.type_competition = type_competition
        self.categorie = categorie
        self.type_competition_generique = type_competition_generique

    @staticmethod
    def from_dict(obj: Any) -> CompetitionOrigine:
        assert isinstance(obj, dict)
        id = from_str(obj, "id")
        code = from_str(obj, "code")
        nom = from_str(obj, "nom")
        tc_val = obj.get("typeCompetition")
        type_competition = (
            CompetitionOrigineTypeCompetition.parse(tc_val)
            if tc_val is not None
            else None
        )
        categorie = from_obj(CompetitionOrigineCategorie.from_dict, obj, "categorie")
        type_competition_generique = from_obj(
            CompetitionOrigineTypeCompetitionGenerique.from_dict,
            obj,
            "typeCompetitionGenerique",
        )
        return CompetitionOrigine(
            id, code, nom, type_competition, categorie, type_competition_generique
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.code is not None:
            result["code"] = self.code
        if self.nom is not None:
            result["nom"] = self.nom
        if self.type_competition is not None:
            result["typeCompetition"] = self.type_competition.value
        if self.categorie is not None:
            result["categorie"] = self.categorie.to_dict()
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = (
                self.type_competition_generique.to_dict()
            )
        return result
