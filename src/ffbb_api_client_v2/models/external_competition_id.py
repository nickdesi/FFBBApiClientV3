from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import (
    from_str,
)


@dataclass
class ExternalCompetitionID:
    code: str | None = None
    nom: str | None = None
    sexe: str | None = None
    type_competition: str | None = None

    @staticmethod
    def from_dict(obj: Any) -> ExternalCompetitionID:
        assert isinstance(obj, dict)
        code = from_str(obj, "code")
        nom = from_str(obj, "nom")
        sexe = from_str(obj, "sexe")
        type_competition = from_str(obj, "typeCompetition")
        return ExternalCompetitionID(
            code=code,
            nom=nom,
            sexe=sexe,
            type_competition=type_competition,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = self.code
        if self.nom is not None:
            result["nom"] = self.nom
        if self.sexe is not None:
            result["sexe"] = self.sexe
        if self.type_competition is not None:
            result["typeCompetition"] = self.type_competition
        return result
