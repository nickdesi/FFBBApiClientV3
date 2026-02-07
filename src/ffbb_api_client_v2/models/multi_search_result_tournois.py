from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from ..utils.converter_utils import (
    from_bool,
    from_datetime,
    from_enum,
    from_int,
    from_obj,
    from_str,
)
from .cartographie import Cartographie
from .commune import Commune
from .facet_distribution import FacetDistribution
from .facet_stats import FacetStats
from .geo import Geo
from .hit import Hit
from .multi_search_result_terrains import TournoiTypes3X3Libelle
from .multi_search_results import MultiSearchResult
from .nature_sol import NatureSol
from .tournoi_type_class import TournoiTypeClass


class SexeClass:
    feminine: int | None = None
    masculine: int | None = None
    mixed: int | None = None

    def __init__(
        self, feminine: int | None, masculine: int | None, mixed: int | None
    ) -> None:
        self.feminine = feminine
        self.masculine = masculine
        self.mixed = mixed

    @staticmethod
    def from_dict(obj: Any) -> SexeClass:
        assert isinstance(obj, dict)
        feminine = from_int(obj, "Féminin")
        masculine = from_int(obj, "Masculin")
        mixed = from_int(obj, "Mixte")
        return SexeClass(feminine, masculine, mixed)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.feminine is not None:
            result["Féminin"] = self.feminine
        if self.masculine is not None:
            result["Masculin"] = self.masculine
        if self.mixed is not None:
            result["Mixte"] = self.mixed
        return result


class TournoisFacetDistribution(FacetDistribution):
    sexe: SexeClass | None = None
    tournoi_type: TournoiTypeClass | None = None
    tournoi_types3_x3_libelle: TournoiTypes3X3Libelle | None = None

    def __init__(
        self,
        sexe: SexeClass | None,
        tournoi_type: TournoiTypeClass | None,
        tournoi_types3_x3_libelle: TournoiTypes3X3Libelle | None,
    ) -> None:
        self.sexe = sexe
        self.tournoi_type = tournoi_type
        self.tournoi_types3_x3_libelle = tournoi_types3_x3_libelle

    @staticmethod
    def from_dict(obj: Any) -> TournoisFacetDistribution:
        assert isinstance(obj, dict)
        sexe = from_obj(SexeClass.from_dict, obj, "sexe")
        tournoi_type = from_obj(TournoiTypeClass.from_dict, obj, "tournoiType")
        tournoi_types3_x3_libelle = from_obj(
            TournoiTypes3X3Libelle.from_dict, obj, "tournoiTypes3x3.libelle"
        )
        return TournoisFacetDistribution(sexe, tournoi_type, tournoi_types3_x3_libelle)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.sexe is not None:
            result["sexe"] = self.sexe.to_dict()
        if self.tournoi_type is not None:
            result["tournoiType"] = self.tournoi_type.to_dict()
        if self.tournoi_types3_x3_libelle is not None:
            result["tournoiTypes3x3.libelle"] = self.tournoi_types3_x3_libelle.to_dict()
        return result


class Libelle(Enum):
    BITUME = "BITUME"
    BÉTON = "Béton"
    SOL_SYNTHÉTIQUE = "Sol synthétique"


class HitType(Enum):
    TERRAIN = "Terrain"


class TournoisHit(Hit):
    nom: str | None = None
    rue: str | None = None
    id: int | None = None
    acces_libre: bool | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    largeur: int | None = None
    longueur: int | None = None
    numero: int | None = None
    cartographie: Cartographie | None = None
    commune: Commune | None = None
    nature_sol: NatureSol | None = None
    geo: Geo | None = None
    thumbnail: str | None = None
    type: HitType | None = None

    def __init__(
        self,
        nom: str | None,
        rue: str | None,
        id: int | None,
        acces_libre: bool | None,
        date_created: datetime | None,
        date_updated: datetime | None,
        largeur: int | None,
        longueur: int | None,
        numero: int | None,
        cartographie: Cartographie | None,
        commune: Commune | None,
        nature_sol: NatureSol | None,
        geo: Geo | None,
        thumbnail: str | None,
        type: HitType | None,
    ) -> None:
        self.nom = nom
        self.rue = rue
        self.lower_nom = nom.lower() if nom else None
        self.lower_rue = rue.lower() if rue else None
        self.id = id
        self.acces_libre = acces_libre
        self.date_created = date_created
        self.date_updated = date_updated
        self.largeur = largeur
        self.longueur = longueur
        self.numero = numero
        self.cartographie = cartographie
        self.commune = commune
        self.nature_sol = nature_sol
        self.geo = geo
        self.thumbnail = thumbnail
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> TournoisHit:
        assert isinstance(obj, dict)
        nom = from_str(obj, "nom")
        rue = from_str(obj, "rue")
        id = from_int(obj, "id")
        acces_libre = from_bool(obj, "accesLibre")
        date_created = from_datetime(obj, "date_created")
        date_updated = from_datetime(obj, "date_updated")
        largeur = from_int(obj, "largeur")
        longueur = from_int(obj, "longueur")
        numero = from_int(obj, "numero")
        cartographie = from_obj(Cartographie.from_dict, obj, "cartographie")
        commune = from_obj(Commune.from_dict, obj, "commune")
        nature_sol = from_obj(NatureSol.from_dict, obj, "natureSol")
        geo = from_obj(Geo.from_dict, obj, "_geo")
        thumbnail = from_str(obj, "thumbnail")
        type = from_enum(HitType, obj, "type")
        return TournoisHit(
            nom,
            rue,
            id,
            acces_libre,
            date_created,
            date_updated,
            largeur,
            longueur,
            numero,
            cartographie,
            commune,
            nature_sol,
            geo,
            thumbnail,
            type,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = self.nom
        if self.rue is not None:
            result["rue"] = self.rue
        if self.id is not None:
            result["id"] = str(self.id)
        if self.acces_libre is not None:
            result["accesLibre"] = self.acces_libre
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.largeur is not None:
            result["largeur"] = self.largeur
        if self.longueur is not None:
            result["longueur"] = self.longueur
        if self.numero is not None:
            result["numero"] = self.numero
        if self.cartographie is not None:
            result["cartographie"] = self.cartographie.to_dict()
        if self.commune is not None:
            result["commune"] = self.commune.to_dict()
        if self.nature_sol is not None:
            result["natureSol"] = self.nature_sol.to_dict()
        if self.geo is not None:
            result["_geo"] = self.geo.to_dict()
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        if self.type is not None:
            result["type"] = self.type.value
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
            not query
            or (self.lower_nom and query in self.lower_nom)
            or (self.lower_rue and query in self.lower_rue)
            or (
                self.commune
                and (
                    (self.commune.lower_libelle and query in self.commune.lower_libelle)
                    or (
                        self.commune.lower_departement
                        and query in self.commune.lower_departement
                    )
                )
            )
        )


class TournoisFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> TournoisFacetStats:
        return TournoisFacetStats()

    def to_dict(self) -> dict:
        return super().to_dict()


class TournoisMultiSearchResult(
    MultiSearchResult[TournoisHit, TournoisFacetDistribution, TournoisFacetStats]
):
    """MultiSearchResult for Tournois."""
