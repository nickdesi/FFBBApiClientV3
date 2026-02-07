from __future__ import annotations

from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_datetime,
    from_obj,
    from_str,
)
from .cartographie import Cartographie
from .commune import Commune
from .facet_distribution import FacetDistribution
from .facet_stats import FacetStats
from .geo import Geo
from .hit import Hit
from .multi_search_results import MultiSearchResult
from .type_association import TypeAssociation

# class LibelleEnum(Enum):
#     SALLE = "Salle"


class SallesFacetDistribution(FacetDistribution):
    @staticmethod
    def from_dict(obj: Any) -> SallesFacetDistribution:
        return SallesFacetDistribution()

    def to_dict(self) -> dict:
        return super().to_dict()


class SallesHit(Hit):
    libelle: str | None = None
    adresse: str | None = None
    id: str | None = None
    adresse_complement: str | None = None
    capacite_spectateur: str | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    libelle2: str | None = None
    mail: str | None = None
    numero: str | None = None
    telephone: str | None = None
    cartographie: Cartographie | None = None
    commune: Commune | None = None
    geo: Geo | None = None
    thumbnail: str | None = None
    type: str | None = None
    type_association: TypeAssociation | None = None

    def __init__(
        self,
        libelle: str | None,
        adresse: str | None,
        id: str | None,
        adresse_complement: str | None,
        capacite_spectateur: str | None,
        date_created: datetime | None,
        date_updated: datetime | None,
        libelle2: str | None,
        mail: str | None,
        numero: str | None,
        telephone: str | None,
        cartographie: Cartographie | None,
        commune: Commune | None,
        geo: Geo | None,
        thumbnail: str | None,
        type: str | None,
        type_association: TypeAssociation | None,
    ) -> None:
        self.libelle = libelle
        self.lower_libelle = libelle.lower() if libelle else None

        self.adresse = adresse
        self.lower_addresse = adresse.lower() if adresse else None

        self.id = id
        self.adresse_complement = adresse_complement
        self.lower_adresse_complement = (
            adresse_complement.lower() if adresse_complement else None
        )

        self.capacite_spectateur = capacite_spectateur
        self.date_created = date_created
        self.date_updated = date_updated
        self.libelle2 = libelle2
        self.lower_libelle2 = libelle2.lower() if libelle2 else None

        self.mail = mail
        self.numero = numero
        self.telephone = telephone
        self.cartographie = cartographie
        self.commune = commune
        self.geo = geo
        self.thumbnail = thumbnail
        self.type = type
        self.type_association = type_association

    @staticmethod
    def from_dict(obj: Any) -> SallesHit:
        assert isinstance(obj, dict)
        libelle = from_str(obj, "libelle")
        adresse = from_str(obj, "adresse")
        id = from_str(obj, "id")
        adresse_complement = from_str(obj, "adresseComplement")
        capacite_spectateur = from_str(obj, "capaciteSpectateur")
        date_created = from_datetime(obj, "date_created")
        date_updated = from_datetime(obj, "date_updated")
        libelle2 = from_str(obj, "libelle2")
        mail = from_str(obj, "mail")
        numero = from_str(obj, "numero")
        telephone = from_str(obj, "telephone")
        cartographie = from_obj(Cartographie.from_dict, obj, "cartographie")
        commune = from_obj(Commune.from_dict, obj, "commune")
        geo = from_obj(Geo.from_dict, obj, "_geo")
        thumbnail = from_str(obj, "thumbnail")
        type = from_str(obj, "type")
        type_association = from_obj(TypeAssociation.from_dict, obj, "type_association")
        return SallesHit(
            libelle,
            adresse,
            id,
            adresse_complement,
            capacite_spectateur,
            date_created,
            date_updated,
            libelle2,
            mail,
            numero,
            telephone,
            cartographie,
            commune,
            geo,
            thumbnail,
            type,
            type_association,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.libelle is not None:
            result["libelle"] = self.libelle
        if self.adresse is not None:
            result["adresse"] = self.adresse
        if self.id is not None:
            result["id"] = self.id
        if self.adresse_complement is not None:
            result["adresseComplement"] = self.adresse_complement
        if self.capacite_spectateur is not None:
            result["capaciteSpectateur"] = self.capacite_spectateur
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.libelle2 is not None:
            result["libelle2"] = self.libelle2
        if self.mail is not None:
            result["mail"] = self.mail
        if self.numero is not None:
            result["numero"] = self.numero
        if self.telephone is not None:
            result["telephone"] = self.telephone
        if self.cartographie is not None:
            result["cartographie"] = self.cartographie.to_dict()
        if self.commune is not None:
            result["commune"] = self.commune.to_dict()
        if self.geo is not None:
            result["_geo"] = self.geo.to_dict()
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        if self.type is not None:
            result["type"] = self.type
        if self.type_association is not None:
            result["type_association"] = self.type_association.to_dict()
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
            not query
            or (self.lower_addresse and query in self.lower_addresse)
            or (
                self.lower_adresse_complement and query in self.lower_adresse_complement
            )
            or (self.lower_libelle and query in self.lower_libelle)
            or (self.lower_libelle2 and query in self.lower_libelle2)
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


class SallesFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> SallesFacetStats:
        return SallesFacetStats()

    def to_dict(self) -> dict:
        return super().to_dict()


class SallesMultiSearchResult(
    MultiSearchResult[SallesHit, SallesFacetDistribution, SallesFacetStats]
):
    """MultiSearchResult for Salles."""
