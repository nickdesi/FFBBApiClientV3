from __future__ import annotations

from typing import Any

from ..utils.converter_utils import (
    from_bool,
    from_obj,
    from_str,
)
from .competition_id_categorie import CompetitionIDCategorie
from .competition_id_type_competition_generique import (
    CompetitionIDTypeCompetitionGenerique,
)
from .competition_origine import CompetitionOrigine
from .logo import Logo


class CompetitionID:
    id: str | None = None
    nom: str | None = None
    competition_origine_nom: str | None = None
    code: str | None = None
    creation_en_cours: bool | None = None
    live_stat: bool | None = None
    publication_internet: str | None = None
    sexe: str | None = None
    type_competition: str | None = None
    pro: bool | None = None
    logo: Logo | None = None
    categorie: CompetitionIDCategorie | None = None
    type_competition_generique: CompetitionIDTypeCompetitionGenerique | None = None
    competition_origine: CompetitionOrigine | None = None
    nom_extended: str | None = None

    def __init__(
        self,
        id: str | None,
        nom: str | None,
        competition_origine_nom: str | None,
        code: str | None,
        creation_en_cours: bool | None,
        live_stat: bool | None,
        publication_internet: str | None,
        sexe: str | None,
        type_competition: str | None,
        pro: bool | None,
        logo: Logo | None,
        categorie: CompetitionIDCategorie | None,
        type_competition_generique: CompetitionIDTypeCompetitionGenerique | None,
        competition_origine: CompetitionOrigine | None,
        nom_extended: str | None,
    ) -> None:
        self.id = id
        self.nom = nom
        self.competition_origine_nom = competition_origine_nom
        self.code = code
        self.creation_en_cours = creation_en_cours
        self.live_stat = live_stat
        self.publication_internet = publication_internet
        self.sexe = sexe
        self.type_competition = type_competition
        self.pro = pro
        self.logo = logo
        self.categorie = categorie
        self.type_competition_generique = type_competition_generique
        self.competition_origine = competition_origine
        self.nom_extended = nom_extended

    @staticmethod
    def from_dict(obj: Any) -> CompetitionID:
        try:
            assert isinstance(obj, dict)
            id = from_str(obj, "id")
            nom = from_str(obj, "nom")
            competition_origine_nom = from_str(obj, "competition_origine_nom")
            code = from_str(obj, "code")
            creation_en_cours = from_bool(obj, "creationEnCours")
            live_stat = from_bool(obj, "liveStat")
            publication_internet = from_str(obj, "publicationInternet")
            sexe = from_str(obj, "sexe")
            type_competition = from_str(obj, "typeCompetition")
            pro = from_bool(obj, "pro")
            logo = from_obj(Logo.from_dict, obj, "logo")
            categorie = from_obj(CompetitionIDCategorie.from_dict, obj, "categorie")
            type_competition_generique = from_obj(
                CompetitionIDTypeCompetitionGenerique.from_dict,
                obj,
                "typeCompetitionGenerique",
            )
            competition_origine = from_obj(
                CompetitionOrigine.from_dict, obj, "competition_origine"
            )
            nom_extended = from_str(obj, "nomExtended")
            return CompetitionID(
                id,
                nom,
                competition_origine_nom,
                code,
                creation_en_cours,
                live_stat,
                publication_internet,
                sexe,
                type_competition,
                pro,
                logo,
                categorie,
                type_competition_generique,
                competition_origine,
                nom_extended,
            )
        except Exception as e:
            raise ValueError("Invalid CompetitionID object") from e

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.nom is not None:
            result["nom"] = self.nom
        if self.competition_origine_nom is not None:
            result["competition_origine_nom"] = self.competition_origine_nom
        if self.code is not None:
            result["code"] = self.code
        if self.creation_en_cours is not None:
            result["creationEnCours"] = self.creation_en_cours
        if self.live_stat is not None:
            result["liveStat"] = self.live_stat
        if self.publication_internet is not None:
            result["publicationInternet"] = self.publication_internet
        if self.sexe is not None:
            result["sexe"] = self.sexe
        if self.type_competition is not None:
            result["typeCompetition"] = self.type_competition
        if self.pro is not None:
            result["pro"] = self.pro
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        if self.categorie is not None:
            result["categorie"] = self.categorie.to_dict()
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = (
                self.type_competition_generique.to_dict()
            )
        if self.competition_origine is not None:
            result["competition_origine"] = self.competition_origine.to_dict()
        if self.nom_extended is not None:
            result["nomExtended"] = self.nom_extended
        return result
