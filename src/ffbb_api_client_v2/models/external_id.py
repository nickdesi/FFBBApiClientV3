from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import (
    from_int,
    from_obj,
    from_str,
)
from .external_competition_id import ExternalCompetitionID
from .id_organisme_equipe import IDOrganismeEquipe
from .id_poule import IDPoule
from .salle import Salle


@dataclass
class ExternalID:
    nom_equipe1: str | None = None
    nom_equipe2: str | None = None
    numero_journee: int | None = None
    competition_id: ExternalCompetitionID | None = None
    id_organisme_equipe1: IDOrganismeEquipe | None = None
    id_organisme_equipe2: IDOrganismeEquipe | None = None
    salle: Salle | None = None
    id_poule: IDPoule | None = None

    @staticmethod
    def from_dict(obj: Any) -> ExternalID:
        assert isinstance(obj, dict)
        nom_equipe1 = from_str(obj, "nomEquipe1")
        nom_equipe2 = from_str(obj, "nomEquipe2")
        numero_journee = from_int(obj, "numeroJournee")
        competition_id = from_obj(ExternalCompetitionID.from_dict, obj, "competitionId")
        id_organisme_equipe1 = from_obj(
            IDOrganismeEquipe.from_dict, obj, "idOrganismeEquipe1"
        )
        id_organisme_equipe2 = from_obj(
            IDOrganismeEquipe.from_dict, obj, "idOrganismeEquipe2"
        )
        salle = from_obj(Salle.from_dict, obj, "salle")
        id_poule = from_obj(IDPoule.from_dict, obj, "idPoule")
        return ExternalID(
            nom_equipe1=nom_equipe1,
            nom_equipe2=nom_equipe2,
            numero_journee=numero_journee,
            competition_id=competition_id,
            id_organisme_equipe1=id_organisme_equipe1,
            id_organisme_equipe2=id_organisme_equipe2,
            salle=salle,
            id_poule=id_poule,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom_equipe1 is not None:
            result["nomEquipe1"] = self.nom_equipe1
        if self.nom_equipe2 is not None:
            result["nomEquipe2"] = self.nom_equipe2
        if self.numero_journee is not None:
            result["numeroJournee"] = str(self.numero_journee)
        if self.competition_id is not None:
            result["competitionId"] = self.competition_id.to_dict()
        if self.id_organisme_equipe1 is not None:
            result["idOrganismeEquipe1"] = self.id_organisme_equipe1.to_dict()
        if self.id_organisme_equipe2 is not None:
            result["idOrganismeEquipe2"] = self.id_organisme_equipe2.to_dict()
        if self.salle is not None:
            result["salle"] = self.salle.to_dict()
        if self.id_poule is not None:
            result["idPoule"] = self.id_poule.to_dict()
        return result
