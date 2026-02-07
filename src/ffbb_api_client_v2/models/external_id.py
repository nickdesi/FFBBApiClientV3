from __future__ import annotations

from typing import Any

from ..utils.converter_utils import (
    from_int,
    from_obj,
    from_str,
)
from .id_organisme_equipe import IDOrganismeEquipe
from .id_poule import IDPoule
from .salle import Salle


class CompetitionID:
    code: str | None = None
    nom: str | None = None
    sexe: str | None = None
    type_competition: str | None = None

    def __init__(
        self,
        code: str | None,
        nom: str | None,
        sexe: str | None,
        type_competition: str | None,
    ) -> None:
        self.code = code
        self.nom = nom
        self.sexe = sexe
        self.type_competition = type_competition

    @staticmethod
    def from_dict(obj: Any) -> CompetitionID:
        assert isinstance(obj, dict)
        code = from_str(obj, "code")
        nom = from_str(obj, "nom")
        sexe = from_str(obj, "sexe")
        type_competition = from_str(obj, "typeCompetition")
        return CompetitionID(code, nom, sexe, type_competition)

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


class ExternalID:
    nom_equipe1: str | None = None
    nom_equipe2: str | None = None
    numero_journee: int | None = None
    competition_id: CompetitionID | None = None
    id_organisme_equipe1: IDOrganismeEquipe | None = None
    id_organisme_equipe2: IDOrganismeEquipe | None = None
    salle: Salle | None = None
    id_poule: IDPoule | None = None

    def __init__(
        self,
        nom_equipe1: str | None,
        nom_equipe2: str | None,
        numero_journee: int | None,
        competition_id: CompetitionID | None,
        id_organisme_equipe1: IDOrganismeEquipe | None,
        id_organisme_equipe2: IDOrganismeEquipe | None,
        salle: Salle | None,
        id_poule: IDPoule | None,
    ) -> None:
        self.nom_equipe1 = nom_equipe1
        self.nom_equipe2 = nom_equipe2
        self.numero_journee = numero_journee
        self.competition_id = competition_id
        self.id_organisme_equipe1 = id_organisme_equipe1
        self.id_organisme_equipe2 = id_organisme_equipe2
        self.salle = salle
        self.id_poule = id_poule

    @staticmethod
    def from_dict(obj: Any) -> ExternalID:
        """
        Construct a new ExternalID object from a dictionary.

        Args:
            obj (Any): The input dictionary.

        Returns:
            ExternalID: The constructed ExternalID object.
        """
        assert isinstance(obj, dict)
        nom_equipe1 = from_str(obj, "nomEquipe1")
        nom_equipe2 = from_str(obj, "nomEquipe2")
        numero_journee = from_int(obj, "numeroJournee")
        competition_id = from_obj(CompetitionID.from_dict, obj, "competitionId")
        id_organisme_equipe1 = from_obj(
            IDOrganismeEquipe.from_dict, obj, "idOrganismeEquipe1"
        )
        id_organisme_equipe2 = from_obj(
            IDOrganismeEquipe.from_dict, obj, "idOrganismeEquipe2"
        )
        salle = from_obj(Salle.from_dict, obj, "salle")
        id_poule = from_obj(IDPoule.from_dict, obj, "idPoule")
        return ExternalID(
            nom_equipe1,
            nom_equipe2,
            numero_journee,
            competition_id,
            id_organisme_equipe1,
            id_organisme_equipe2,
            salle,
            id_poule,
        )

    def to_dict(self) -> dict:
        """
        Convert the ExternalID object to a dictionary.

        Returns:
            dict: The converted dictionary.
        """
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
