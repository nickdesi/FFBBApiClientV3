from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from ..utils.converter_utils import (
    from_bool,
    from_datetime,
    from_list,
    from_obj,
    from_str,
)
from .cartographie import Cartographie
from .commune import Commune
from .facet_distribution import FacetDistribution
from .facet_stats import FacetStats
from .geo import Geo
from .hit import Hit
from .labellisation import Labellisation
from .logo import Logo
from .multi_search_results import MultiSearchResult
from .organisme_id_pere import OrganismeIDPere
from .type_association import TypeAssociation
from .type_association_libelle import TypeAssociationLibelle
from .type_class import TypeClass


class OrganismesFacetDistribution(FacetDistribution):
    labellisation: Labellisation | None = None
    offres_pratiques: dict[str, int] | None = None
    type: TypeClass | None = None
    type_association_libelle: TypeAssociationLibelle | None = None

    def __init__(
        self,
        labellisation: Labellisation | None,
        offres_pratiques: dict[str, int] | None,
        type: TypeClass | None,
        type_association_libelle: TypeAssociationLibelle | None,
    ) -> None:
        self.labellisation = labellisation
        self.offres_pratiques = offres_pratiques
        self.type = type
        self.type_association_libelle = type_association_libelle

    @staticmethod
    def from_dict(obj: Any) -> OrganismesFacetDistribution:
        assert isinstance(obj, dict)
        labellisation = from_obj(Labellisation.from_dict, obj, "labellisation")
        offres_pratiques = obj.get("offresPratiques")
        type = from_obj(TypeClass.from_dict, obj, "type")
        type_association_libelle = from_obj(
            TypeAssociationLibelle.from_dict, obj, "type_association.libelle"
        )
        return OrganismesFacetDistribution(
            labellisation, offres_pratiques, type, type_association_libelle
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.labellisation is not None:
            result["labellisation"] = self.labellisation.to_dict()
        if self.offres_pratiques is not None:
            result["offresPratiques"] = self.offres_pratiques
        if self.type is not None:
            result["type"] = self.type.to_dict()
        if self.type_association_libelle is not None:
            result["type_association.libelle"] = self.type_association_libelle.to_dict()
        return result


class HitType(Enum):
    BASKET_INCLUSIF = "Basket Inclusif"
    BASKET_SANTÉ = "Basket Santé"
    BASKET_TONIK = "Basket Tonik"
    CENTRE_GÉNÉRATION_BASKET = "Centre Génération Basket"
    MICRO_BASKET = "Micro Basket"


class OrganismesHit(Hit):
    nom_club_pro: str | None = None
    nom: str | None = None
    adresse: str | None = None
    adresse_club_pro: str | None = None
    code: str | None = None
    id: str | None = None
    engagements_noms: str | None = None
    mail: str | None = None
    telephone: str | None = None
    type: str | None = None
    url_site_web: str | None = None
    nom_simple: str | None = None
    date_affiliation: datetime | None = None
    saison_en_cours: bool | None = None
    offres_pratiques: list[str] | None = None
    labellisation: list[str] | None = None
    cartographie: Cartographie | None = None
    organisme_id_pere: OrganismeIDPere | None = None
    commune: Commune | None = None
    commune_club_pro: Commune | None = None
    type_association: TypeAssociation | None = None
    logo: Logo | None = None
    geo: Geo | None = None
    thumbnail: str | None = None

    def __init__(
        self,
        nom_club_pro: str | None,
        nom: str | None,
        adresse: str | None,
        adresse_club_pro: str | None,
        code: str | None,
        id: str | None,
        engagements_noms: str | None,
        mail: str | None,
        telephone: str | None,
        type: str | None,
        url_site_web: str | None,
        nom_simple: str | None,
        date_affiliation: datetime | None,
        saison_en_cours: bool | None,
        offres_pratiques: list[str] | None,
        labellisation: list[str] | None,
        cartographie: Cartographie | None,
        organisme_id_pere: OrganismeIDPere | None,
        commune: Commune | None,
        commune_club_pro: Commune | None,
        type_association: TypeAssociation | None,
        logo: Logo | None,
        geo: Geo | None,
        thumbnail: str | None,
    ) -> None:
        self.nom_club_pro = nom_club_pro
        self.lower_nom_club_pro = nom_club_pro.lower() if nom_club_pro else None

        self.nom = nom
        self.lower_nom = nom.lower() if nom else None

        self.adresse = adresse
        self.adresse_club_pro = adresse_club_pro
        self.code = code
        self.id = id
        self.engagements_noms = engagements_noms
        self.lower_engagements_noms = (
            self.engagements_noms.lower() if self.engagements_noms else None
        )

        self.mail = mail
        self.telephone = telephone
        self.type = type
        self.url_site_web = url_site_web
        self.nom_simple = nom_simple
        self.date_affiliation = date_affiliation
        self.saison_en_cours = saison_en_cours
        self.offres_pratiques = offres_pratiques
        self.labellisation = labellisation
        self.cartographie = cartographie
        self.organisme_id_pere = organisme_id_pere
        self.commune = commune
        self.commune_club_pro = commune_club_pro
        self.type_association = type_association
        self.logo = logo
        self.geo = geo
        self.thumbnail = thumbnail

    @staticmethod
    def from_dict(obj: Any) -> Hit:
        try:
            assert isinstance(obj, dict)
            nom_club_pro = from_str(obj, "nomClubPro")
            nom = from_str(obj, "nom")
            adresse = from_str(obj, "adresse")
            adresse_club_pro = from_str(obj, "adresseClubPro")
            code = from_str(obj, "code")
            id = from_str(obj, "id")
            engagements_noms = from_str(obj, "engagements_noms")
            mail = from_str(obj, "mail")
            telephone = from_str(obj, "telephone")
            type = from_str(obj, "type")
            url_site_web = from_str(obj, "urlSiteWeb")
            nom_simple = from_str(obj, "nom_simple")
            date_affiliation = from_datetime(obj, "dateAffiliation")
            saison_en_cours = from_bool(obj, "saison_en_cours")
            offres_pratiques = from_list(str, obj, "offresPratiques")
            labellisation = from_list(str, obj, "labellisation")
            cartographie = from_obj(Cartographie.from_dict, obj, "cartographie")
            organisme_id_pere = from_obj(
                OrganismeIDPere.from_dict, obj, "organisme_id_pere"
            )
            commune = from_obj(Commune.from_dict, obj, "commune")
            commune_club_pro = from_obj(Commune.from_dict, obj, "communeClubPro")
            type_association = from_obj(
                TypeAssociation.from_dict, obj, "type_association"
            )
            logo = from_obj(Logo.from_dict, obj, "logo")
            geo = from_obj(Geo.from_dict, obj, "_geo")
            thumbnail = from_str(obj, "thumbnail")
            return OrganismesHit(
                nom_club_pro,
                nom,
                adresse,
                adresse_club_pro,
                code,
                id,
                engagements_noms,
                mail,
                telephone,
                type,
                url_site_web,
                nom_simple,
                date_affiliation,
                saison_en_cours,
                offres_pratiques,
                labellisation,
                cartographie,
                organisme_id_pere,
                commune,
                commune_club_pro,
                type_association,
                logo,
                geo,
                thumbnail,
            )
        except Exception as e:
            raise ValueError(f"Invalid `OrganismesHit` object: {e}") from e

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom_club_pro is not None:
            result["nomClubPro"] = self.nom_club_pro
        if self.nom is not None:
            result["nom"] = self.nom
        if self.adresse is not None:
            result["adresse"] = self.adresse
        if self.adresse_club_pro is not None:
            result["adresseClubPro"] = self.adresse_club_pro
        if self.code is not None:
            result["code"] = self.code
        if self.id is not None:
            result["id"] = self.id
        if self.engagements_noms is not None:
            result["engagements_noms"] = self.engagements_noms
        if self.mail is not None:
            result["mail"] = self.mail
        if self.telephone is not None:
            result["telephone"] = self.telephone
        if self.type is not None:
            result["type"] = self.type
        if self.url_site_web is not None:
            result["urlSiteWeb"] = self.url_site_web
        if self.nom_simple is not None:
            result["nom_simple"] = self.nom_simple
        if self.date_affiliation is not None:
            result["dateAffiliation"] = self.date_affiliation.isoformat()
        if self.saison_en_cours is not None:
            result["saison_en_cours"] = self.saison_en_cours
        if self.offres_pratiques is not None:
            result["offresPratiques"] = self.offres_pratiques
        if self.labellisation is not None:
            result["labellisation"] = self.labellisation
        if self.cartographie is not None:
            result["cartographie"] = self.cartographie.to_dict()
        if self.organisme_id_pere is not None:
            result["organisme_id_pere"] = self.organisme_id_pere.to_dict()
        if self.commune is not None:
            result["commune"] = self.commune.to_dict()
        if self.commune_club_pro is not None:
            result["communeClubPro"] = self.commune_club_pro.to_dict()
        if self.type_association is not None:
            result["type_association"] = self.type_association.to_dict()
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        if self.geo is not None:
            result["_geo"] = self.geo.to_dict()
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
            not query
            or (self.lower_nom and query in self.lower_nom)
            or (self.lower_nom_club_pro and query in self.lower_nom_club_pro)
            or (self.lower_engagements_noms and query in self.lower_engagements_noms)
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


class OrganismesFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> OrganismesFacetStats:
        return OrganismesFacetStats()

    def to_dict(self) -> dict:
        return super().to_dict()


class OrganismesMultiSearchResult(
    MultiSearchResult[OrganismesHit, OrganismesFacetDistribution, OrganismesFacetStats]
):
    """MultiSearchResult for Organismes."""
