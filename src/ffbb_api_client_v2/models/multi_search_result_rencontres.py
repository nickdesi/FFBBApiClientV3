from __future__ import annotations

from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_datetime,
    from_enum,
    from_int,
    from_obj,
    from_officiels_list,
    from_str,
)
from .competition_id import CompetitionID
from .competition_id_sexe import CompetitionIDSexe
from .competition_id_type_competition import CompetitionIDTypeCompetition
from .facet_distribution import FacetDistribution
from .facet_stats import FacetStats
from .geo import Geo
from .hit import Hit
from .id_engagement_equipe import IDEngagementEquipe
from .id_organisme_equipe import IDOrganismeEquipe
from .id_poule import IDPoule
from .multi_search_results import MultiSearchResult
from .niveau import Niveau
from .niveau_class import NiveauClass
from .organisateur import Organisateur
from .pratique import Pratique
from .saison import Saison
from .salle import Salle


class RencontresFacetDistribution(FacetDistribution):
    competition_id_categorie_code: dict[str, int] | None = None
    competition_id_nom_extended: dict[str, int] | None = None
    competition_id_sexe: CompetitionIDSexe | None = None
    competition_id_type_competition: CompetitionIDTypeCompetition | None = None
    niveau: NiveauClass | None = None
    organisateur_id: dict[str, int] | None = None
    organisateur_nom: dict[str, int] | None = None

    def __init__(
        self,
        competition_id_categorie_code: dict[str, int] | None,
        competition_id_nom_extended: dict[str, int] | None,
        competition_id_sexe: CompetitionIDSexe | None,
        competition_id_type_competition: CompetitionIDTypeCompetition | None,
        niveau: NiveauClass | None,
        organisateur_id: dict[str, int] | None,
        organisateur_nom: dict[str, int] | None,
    ):
        self.competition_id_categorie_code = competition_id_categorie_code
        self.competition_id_nom_extended = competition_id_nom_extended
        self.competition_id_sexe = competition_id_sexe
        self.competition_id_type_competition = competition_id_type_competition
        self.niveau = niveau
        self.organisateur_id = organisateur_id
        self.organisateur_nom = organisateur_nom

    @staticmethod
    def from_dict(obj: Any) -> RencontresFacetDistribution:
        assert isinstance(obj, dict)
        competition_id_categorie_code = obj.get("competitionId.categorie.code")
        competition_id_nom_extended = obj.get("competitionId.nomExtended")
        competition_id_sexe = from_obj(
            CompetitionIDSexe.from_dict, obj, "competitionId.sexe"
        )
        competition_id_type_competition = from_obj(
            CompetitionIDTypeCompetition.from_dict, obj, "competitionId.typeCompetition"
        )
        niveau = from_obj(NiveauClass.from_dict, obj, "niveau")
        organisateur_id = obj.get("organisateur.id")
        organisateur_nom = obj.get("organisateur.nom")
        return RencontresFacetDistribution(
            competition_id_categorie_code,
            competition_id_nom_extended,
            competition_id_sexe,
            competition_id_type_competition,
            niveau,
            organisateur_id,
            organisateur_nom,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.competition_id_categorie_code is not None:
            result["competitionId.categorie.code"] = self.competition_id_categorie_code
        if self.competition_id_nom_extended is not None:
            result["competitionId.nomExtended"] = self.competition_id_nom_extended
        if self.competition_id_sexe is not None:
            result["competitionId.sexe"] = self.competition_id_sexe.to_dict()
        if self.competition_id_type_competition is not None:
            result["competitionId.typeCompetition"] = (
                self.competition_id_type_competition.to_dict()
            )
        if self.niveau is not None:
            result["niveau"] = self.niveau.to_dict()
        if self.organisateur_id is not None:
            result["organisateur.id"] = self.organisateur_id
        if self.organisateur_nom is not None:
            result["organisateur.nom"] = self.organisateur_nom
        return result


# class LibelleEnum(Enum):
#     SE = "SE"
#     SENIORS = "Seniors"
#     U11 = "U11"
#     U13 = "U13"
#     U15 = "U15"
#     U17 = "U17"
#     U18 = "U18"
#     U20 = "U20"
#     U7 = "U7"
#     U9 = "U9"
#     VE = "VE"
#     VÉTÉRANS = "Vétérans"


class Engagement:
    id: str | None = None

    def __init__(self, id: str | None):
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> Engagement:
        assert isinstance(obj, dict)
        id = from_str(obj, "id")
        return Engagement(id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        return result


class RencontresHit(Hit):
    niveau: Niveau | None = None
    id: str | None = None
    date: datetime | None = None
    date_rencontre: datetime | None = None
    horaire: int | None = None
    nom_equipe1: str | None = None
    nom_equipe2: str | None = None
    numero_journee: int | None = None
    pratique: Pratique | None = None
    gs_id: str | None = None
    officiels: list[str] | None = None
    competition_id: CompetitionID | None = None
    id_organisme_equipe1: IDOrganismeEquipe | None = None
    id_organisme_equipe2: IDOrganismeEquipe | None = None
    id_poule: IDPoule | None = None
    saison: Saison | None = None
    salle: Salle | None = None
    id_engagement_equipe1: IDEngagementEquipe | None = None
    id_engagement_equipe2: IDEngagementEquipe | None = None
    geo: Geo | None = None
    date_timestamp: int | None = None
    date_rencontre_timestamp: int | None = None
    creation_timestamp: int | None = None
    date_saisie_resultat_timestamp: int | None = None
    modification_timestamp: int | None = None
    thumbnail: str | None = None
    organisateur: Organisateur | None = None
    niveau_nb: int | None = None

    def __init__(
        self,
        niveau: Niveau | None,
        id: str | None,
        date: datetime | None,
        date_rencontre: datetime | None,
        horaire: int | None,
        nom_equipe1: str | None,
        nom_equipe2: str | None,
        numero_journee: int | None,
        pratique: Pratique | None,
        gs_id: str | None,
        officiels: list | None,
        competition_id: CompetitionID | None,
        id_organisme_equipe1: IDOrganismeEquipe | None,
        id_organisme_equipe2: IDOrganismeEquipe | None,
        id_poule: IDPoule | None,
        saison: Saison | None,
        salle: Salle | None,
        id_engagement_equipe1: IDEngagementEquipe | None,
        id_engagement_equipe2: IDEngagementEquipe | None,
        geo: Geo | None,
        date_timestamp: int | None,
        date_rencontre_timestamp: int | None,
        creation_timestamp: int | None,
        date_saisie_resultat_timestamp: int | None,
        modification_timestamp: int | None,
        thumbnail: str | None,
        organisateur: Organisateur | None,
        niveau_nb: int | None,
    ):
        self.niveau = niveau
        self.id = id
        self.lower_id = id.lower() if id else None

        self.date = date
        self.date_rencontre = date_rencontre
        self.horaire = horaire
        self.nom_equipe1 = nom_equipe1
        self.nom_equipe2 = nom_equipe2
        self.lower_nom_equipe1 = nom_equipe1.lower() if nom_equipe1 else None
        self.lower_nom_equipe2 = nom_equipe2.lower() if nom_equipe2 else None

        self.numero_journee = numero_journee
        self.pratique = pratique
        self.gs_id = gs_id
        self.lower_gs_id = gs_id.lower() if gs_id else None

        self.officiels = officiels
        # Handle both old format (list of strings) and new format (list of dicts)
        if officiels:
            lower_officiels = []
            for o in officiels:
                if isinstance(o, str):
                    lower_officiels.append(o.lower())
                elif isinstance(o, dict):
                    # Extract name from dict format: {'officiel': {'nom': '...', 'prenom': '...'}}
                    off = o.get("officiel", {})
                    name = f"{off.get('nom', '')} {off.get('prenom', '')}".strip()
                    lower_officiels.append(name.lower() if name else "")
            self.lower_officiels = lower_officiels if lower_officiels else None
        else:
            self.lower_officiels = None

        self.competition_id = competition_id
        self.id_organisme_equipe1 = id_organisme_equipe1
        self.id_organisme_equipe2 = id_organisme_equipe2
        self.id_poule = id_poule
        self.saison = saison
        self.salle = salle
        self.id_engagement_equipe1 = id_engagement_equipe1
        self.id_engagement_equipe2 = id_engagement_equipe2
        self.geo = geo
        self.date_timestamp = date_timestamp
        self.date_rencontre_timestamp = date_rencontre_timestamp
        self.creation_timestamp = creation_timestamp
        self.date_saisie_resultat_timestamp = date_saisie_resultat_timestamp
        self.modification_timestamp = modification_timestamp
        self.thumbnail = thumbnail
        self.organisateur = organisateur
        self.niveau_nb = niveau_nb

    @staticmethod
    def from_dict(obj: Any) -> Hit:
        try:
            assert isinstance(obj, dict)
            niveau = from_enum(Niveau, obj, "niveau")
            id = from_str(obj, "id")
            date = from_datetime(obj, "date")
            date_rencontre = from_datetime(obj, "date_rencontre")
            horaire = from_int(obj, "horaire")
            nom_equipe1 = from_str(obj, "nomEquipe1")
            nom_equipe2 = from_str(obj, "nomEquipe2")

            numero_journee = from_int(obj, "numeroJournee")
            pratique = from_enum(Pratique, obj, "pratique")
            gs_id = from_str(obj, "gsId")
            officiels = from_officiels_list(obj.get("officiels"))
            competition_id = from_obj(CompetitionID.from_dict, obj, "competitionId")
            id_organisme_equipe1 = from_obj(
                IDOrganismeEquipe.from_dict, obj, "idOrganismeEquipe1"
            )
            id_organisme_equipe2 = from_obj(
                IDOrganismeEquipe.from_dict, obj, "idOrganismeEquipe2"
            )
            id_poule = from_obj(IDPoule.from_dict, obj, "idPoule")
            saison = from_obj(Saison.from_dict, obj, "saison")
            salle = from_obj(Salle.from_dict, obj, "salle")
            id_engagement_equipe1 = from_obj(
                IDEngagementEquipe.from_dict, obj, "idEngagementEquipe1"
            )
            id_engagement_equipe2 = from_obj(
                IDEngagementEquipe.from_dict, obj, "idEngagementEquipe2"
            )
            geo = from_obj(Geo.from_dict, obj, "_geo")
            date_timestamp = from_int(obj, "date_timestamp")
            date_rencontre_timestamp = from_int(obj, "date_rencontre_timestamp")
            creation_timestamp = from_int(obj, "creation_timestamp")
            date_saisie_resultat_timestamp = from_int(
                obj, "dateSaisieResultat_timestamp"
            )
            modification_timestamp = from_int(obj, "modification_timestamp")
            thumbnail = from_str(obj, "thumbnail")
            organisateur = from_obj(Organisateur.from_dict, obj, "organisateur")
            niveau_nb = from_int(obj, "niveau_nb")
            return RencontresHit(
                niveau,
                id,
                date,
                date_rencontre,
                horaire,
                nom_equipe1,
                nom_equipe2,
                numero_journee,
                pratique,
                gs_id,
                officiels,
                competition_id,
                id_organisme_equipe1,
                id_organisme_equipe2,
                id_poule,
                saison,
                salle,
                id_engagement_equipe1,
                id_engagement_equipe2,
                geo,
                date_timestamp,
                date_rencontre_timestamp,
                creation_timestamp,
                date_saisie_resultat_timestamp,
                modification_timestamp,
                thumbnail,
                organisateur,
                niveau_nb,
            )
        except Exception as e:
            raise ValueError(f"Invalid `Hit` object: {e}") from e

    def to_dict(self) -> dict:
        result: dict = {}
        if self.niveau is not None:
            result["niveau"] = self.niveau.value
        if self.id is not None:
            result["id"] = self.id
        if self.date is not None:
            result["date"] = self.date.isoformat()
        if self.date_rencontre is not None:
            result["date_rencontre"] = self.date_rencontre.isoformat()
        if self.horaire is not None:
            result["horaire"] = str(self.horaire)
        if self.nom_equipe1 is not None:
            result["nomEquipe1"] = self.nom_equipe1
        if self.nom_equipe2 is not None:
            result["nomEquipe2"] = self.nom_equipe2
        if self.numero_journee is not None:
            result["numeroJournee"] = str(self.numero_journee)
        if self.pratique is not None:
            result["pratique"] = self.pratique.value
        if self.gs_id is not None:
            result["gsId"] = self.gs_id
        if self.officiels is not None:
            result["officiels"] = self.officiels
        if self.competition_id is not None:
            result["competitionId"] = self.competition_id.to_dict()
        if self.id_organisme_equipe1 is not None:
            result["idOrganismeEquipe1"] = self.id_organisme_equipe1.to_dict()
        if self.id_organisme_equipe2 is not None:
            result["idOrganismeEquipe2"] = self.id_organisme_equipe2.to_dict()
        if self.id_poule is not None:
            result["idPoule"] = self.id_poule.to_dict()
        if self.saison is not None:
            result["saison"] = self.saison.to_dict()
        if self.salle is not None:
            result["salle"] = self.salle.to_dict()
        if self.id_engagement_equipe1 is not None:
            result["idEngagementEquipe1"] = self.id_engagement_equipe1.to_dict()
        if self.id_engagement_equipe2 is not None:
            result["idEngagementEquipe2"] = self.id_engagement_equipe2.to_dict()
        if self.geo is not None:
            result["_geo"] = self.geo.to_dict()
        if self.date_timestamp is not None:
            result["date_timestamp"] = self.date_timestamp
        if self.date_rencontre_timestamp is not None:
            result["date_rencontre_timestamp"] = self.date_rencontre_timestamp
        if self.creation_timestamp is not None:
            result["creation_timestamp"] = self.creation_timestamp
        if self.date_saisie_resultat_timestamp is not None:
            result["dateSaisieResultat_timestamp"] = self.date_saisie_resultat_timestamp
        if self.modification_timestamp is not None:
            result["modification_timestamp"] = self.modification_timestamp
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        if self.organisateur is not None:
            result["organisateur"] = self.organisateur.to_dict()
        if self.niveau_nb is not None:
            result["niveau_nb"] = str(self.niveau_nb)
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
            not query
            or (self.lower_gs_id and query in self.lower_gs_id)
            or (self.lower_id and query in self.lower_id)
            or (
                self.lower_officiels
                and any(query in off for off in self.lower_officiels)
            )
            or (
                self.salle
                and (
                    (self.salle.lower_adresse and query in self.salle.lower_adresse)
                    or (
                        self.salle.lower_adresse_complement
                        and query in self.salle.lower_adresse_complement
                    )
                    or (self.salle.lower_libelle and query in self.salle.lower_libelle)
                )
            )
        )


class RencontresFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> RencontresFacetStats:
        return RencontresFacetStats()

    def to_dict(self) -> dict:
        return super().to_dict()


class RencontresMultiSearchResult(
    MultiSearchResult[RencontresHit, RencontresFacetDistribution, RencontresFacetStats]
):
    """MultiSearchResult for Rencontres."""
