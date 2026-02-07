from __future__ import annotations

from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_bool,
    from_datetime,
    from_enum,
    from_int,
    from_list,
    from_none,
    from_obj,
    from_str,
)
from .categorie import Categorie
from .competition_id_sexe import CompetitionIDSexe
from .competition_id_type_competition import CompetitionIDTypeCompetition
from .etat import Etat
from .facet_distribution import FacetDistribution
from .facet_stats import FacetStats
from .hit import Hit
from .logo import Logo
from .multi_search_results import MultiSearchResult
from .niveau import Niveau
from .niveau_class import NiveauClass
from .organisateur import Organisateur
from .phase_code import PhaseCode
from .poule import Poule
from .publication_internet import PublicationInternet
from .saison import Saison
from .sexe import Sexe
from .type_competition import TypeCompetition
from .type_competition_generique import TypeCompetitionGenerique


class CompetitionsFacetDistribution(FacetDistribution):
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
    ) -> None:
        self.competition_id_categorie_code = competition_id_categorie_code
        self.competition_id_nom_extended = competition_id_nom_extended
        self.competition_id_sexe = competition_id_sexe
        self.competition_id_type_competition = competition_id_type_competition
        self.niveau = niveau
        self.organisateur_id = organisateur_id
        self.organisateur_nom = organisateur_nom

    @staticmethod
    def from_dict(obj: Any) -> CompetitionsFacetDistribution:
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
        return CompetitionsFacetDistribution(
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


class CompetitionsHit(Hit):
    nom: str | None = None
    code: str | None = None
    niveau: Niveau | None = None
    type_competition: TypeCompetition | None = None
    sexe: Sexe | None = None
    id: str | None = None
    creation_en_cours: bool | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    emarque_v2: bool | None = None
    live_stat: bool | None = None
    publication_internet: PublicationInternet | None = None
    pro: bool | None = None
    competition_origine: str | None = None
    competition_origine_niveau: int | None = None
    phase_code: PhaseCode | None = None
    competition_origine_nom: str | None = None
    etat: Etat | None = None
    poules: list[Poule] | None = None
    phases: list[str] | None = None
    categorie: Categorie | None = None
    id_competition_pere: None
    organisateur: Organisateur | None = None
    saison: Saison | None = None
    logo: Logo | None = None
    type_competition_generique: TypeCompetitionGenerique | None = None
    thumbnail: str | None = None
    niveau_nb: int | None = None

    def __init__(
        self,
        nom: str | None,
        code: str | None,
        niveau: Niveau | None,
        type_competition: TypeCompetition | None,
        sexe: Sexe | None,
        id: str | None,
        creation_en_cours: bool | None,
        date_created: datetime | None,
        date_updated: datetime | None,
        emarque_v2: bool | None,
        live_stat: bool | None,
        publication_internet: PublicationInternet | None,
        pro: bool | None,
        competition_origine: str | None,
        competition_origine_niveau: int | None,
        phase_code: PhaseCode | None,
        competition_origine_nom: str | None,
        etat: Etat | None,
        poules: list[Poule] | None,
        phases: list[str] | None,
        categorie: Categorie | None,
        id_competition_pere: None,
        organisateur: Organisateur | None,
        saison: Saison | None,
        logo: Logo | None,
        type_competition_generique: TypeCompetitionGenerique | None,
        thumbnail: str | None,
        niveau_nb: int | None,
    ) -> None:
        self.nom = nom
        self.lower_nom = nom.lower() if nom else None

        self.code = code
        self.lower_code = code.lower() if code else None

        self.niveau = niveau
        self.type_competition = type_competition
        self.sexe = sexe
        self.id = id
        self.lower_id = id.lower() if id else None

        self.creation_en_cours = creation_en_cours
        self.date_created = date_created
        self.date_updated = date_updated
        self.emarque_v2 = emarque_v2
        self.live_stat = live_stat
        self.publication_internet = publication_internet
        self.pro = pro
        self.competition_origine = competition_origine
        self.lower_competition_origine = (
            competition_origine.lower() if competition_origine else None
        )

        self.competition_origine_niveau = competition_origine_niveau
        self.competition_origine_nom = competition_origine_nom
        self.lower_competition_origine_nom = (
            competition_origine_nom.lower() if competition_origine_nom else None
        )

        self.phase_code = phase_code
        self.etat = etat
        self.poules = poules
        self.phases = phases
        self.categorie = categorie
        self.id_competition_pere = id_competition_pere
        self.organisateur = organisateur
        self.saison = saison
        self.logo = logo
        self.type_competition_generique = type_competition_generique
        self.thumbnail = thumbnail
        self.niveau_nb = niveau_nb

    @staticmethod
    def from_dict(obj: Any) -> Hit:
        try:
            assert isinstance(obj, dict)
            nom = from_str(obj, "nom")
            code = from_str(obj, "code")
            niveau = from_enum(Niveau, obj, "niveau")
            type_competition = from_enum(TypeCompetition, obj, "typeCompetition")
            sexe = from_enum(Sexe, obj, "sexe")
            id = from_str(obj, "id")
            creation_en_cours = from_bool(obj, "creationEnCours")
            date_created = from_datetime(obj, "date_created")
            date_updated = from_datetime(obj, "date_updated")
            emarque_v2 = from_bool(obj, "emarqueV2")
            live_stat = from_bool(obj, "liveStat")
            publication_internet = from_enum(
                PublicationInternet, obj, "publicationInternet"
            )
            pro = from_bool(obj, "pro")
            competition_origine = from_str(obj, "competition_origine")
            competition_origine_niveau = from_int(obj, "competition_origine_niveau")
            phase_code = from_enum(PhaseCode, obj, "phase_code")
            competition_origine_nom = from_str(obj, "competition_origine_nom")
            etat = from_enum(Etat, obj, "etat")
            poules = from_list(Poule.from_dict, obj, "poules")
            phases = from_list(str, obj, "phases")
            categorie = from_obj(Categorie.from_dict, obj, "categorie")
            id_competition_pere = from_none(obj.get("idCompetitionPere"))
            organisateur = from_obj(Organisateur.from_dict, obj, "organisateur")
            saison = from_obj(Saison.from_dict, obj, "saison")
            logo = from_obj(Logo.from_dict, obj, "logo")
            type_competition_generique = from_obj(
                TypeCompetitionGenerique.from_dict, obj, "typeCompetitionGenerique"
            )
            thumbnail = from_str(obj, "thumbnail")
            niveau_nb = from_int(obj, "niveau_nb")
            return CompetitionsHit(
                nom,
                code,
                niveau,
                type_competition,
                sexe,
                id,
                creation_en_cours,
                date_created,
                date_updated,
                emarque_v2,
                live_stat,
                publication_internet,
                pro,
                competition_origine,
                competition_origine_niveau,
                phase_code,
                competition_origine_nom,
                etat,
                poules,
                phases,
                categorie,
                id_competition_pere,
                organisateur,
                saison,
                logo,
                type_competition_generique,
                thumbnail,
                niveau_nb,
            )
        except Exception as e:
            raise ValueError(f"Invalid `Hit.from_dict` input: {e}") from e

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = self.nom
        if self.code is not None:
            result["code"] = self.code
        if self.niveau is not None:
            result["niveau"] = self.niveau.value
        if self.type_competition is not None:
            result["typeCompetition"] = self.type_competition.value
        if self.sexe is not None:
            result["sexe"] = self.sexe.value
        if self.id is not None:
            result["id"] = self.id
        if self.creation_en_cours is not None:
            result["creationEnCours"] = self.creation_en_cours
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.emarque_v2 is not None:
            result["emarqueV2"] = self.emarque_v2
        if self.live_stat is not None:
            result["liveStat"] = self.live_stat
        if self.publication_internet is not None:
            result["publicationInternet"] = self.publication_internet.value
        if self.pro is not None:
            result["pro"] = self.pro
        if self.competition_origine is not None:
            result["competition_origine"] = self.competition_origine
        if self.competition_origine_niveau is not None:
            result["competition_origine_niveau"] = self.competition_origine_niveau
        if self.phase_code is not None:
            result["phase_code"] = self.phase_code.value
        if self.competition_origine_nom is not None:
            result["competition_origine_nom"] = self.competition_origine_nom
        if self.etat is not None:
            result["etat"] = self.etat.value
        if self.poules is not None:
            result["poules"] = [p.to_dict() for p in self.poules]
        if self.phases is not None:
            result["phases"] = self.phases
        if self.categorie is not None:
            result["categorie"] = self.categorie.to_dict()
        if self.id_competition_pere is not None:
            result["idCompetitionPere"] = from_none(self.id_competition_pere)
        if self.organisateur is not None:
            result["organisateur"] = self.organisateur.to_dict()
        if self.saison is not None:
            result["saison"] = self.saison.to_dict()
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = (
                self.type_competition_generique.to_dict()
            )
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        if self.niveau_nb is not None:
            result["niveau_nb"] = str(self.niveau_nb)
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
            not query
            or (self.lower_nom and query in self.lower_nom)
            or (self.lower_code and query in self.lower_code)
            or (self.lower_id and query in self.lower_id)
            or (
                self.lower_competition_origine
                and query in self.lower_competition_origine
            )
            or (
                self.lower_competition_origine_nom
                and query in self.lower_competition_origine_nom
            )
        )


class CompetitionsFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> CompetitionsFacetStats:
        return CompetitionsFacetStats()

    def to_dict(self) -> dict:
        return super().to_dict()


class CompetitionsMultiSearchResult(
    MultiSearchResult[
        CompetitionsHit, CompetitionsFacetDistribution, CompetitionsFacetStats
    ]
):
    """MultiSearchResult for Competitions."""
