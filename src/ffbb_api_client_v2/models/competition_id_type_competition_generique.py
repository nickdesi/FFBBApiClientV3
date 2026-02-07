from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_obj
from .id_organisme_equipe1_logo import IDOrganismeEquipe1Logo


class CompetitionIDTypeCompetitionGenerique:
    logo: IDOrganismeEquipe1Logo | None = None

    def __init__(self, logo: IDOrganismeEquipe1Logo | None) -> None:
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> CompetitionIDTypeCompetitionGenerique:
        assert isinstance(obj, dict)
        logo = from_obj(IDOrganismeEquipe1Logo.from_dict, obj, "logo")
        return CompetitionIDTypeCompetitionGenerique(logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        return result
