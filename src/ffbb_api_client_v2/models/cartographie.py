from __future__ import annotations

from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_datetime,
    from_float,
    from_int,
    from_obj,
    from_str,
)
from .coordonnees import Coordonnees


class Cartographie:
    adresse: str | None = None
    code_postal: int | None = None
    coordonnees: Coordonnees | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    cartographie_id: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    title: str | None = None
    ville: str | None = None
    status: str | None = None

    def __init__(
        self,
        adresse: str | None,
        code_postal: int | None,
        coordonnees: Coordonnees | None,
        date_created: datetime | None,
        date_updated: datetime | None,
        id: str | None,
        latitude: float | None,
        longitude: float | None,
        title: str | None,
        ville: str | None,
        status: str | None,
    ):
        self.adresse = adresse
        self.code_postal = code_postal
        self.coordonnees = coordonnees
        self.date_created = date_created
        self.date_updated = date_updated
        self.cartographie_id = id
        self.latitude = latitude
        self.longitude = longitude
        self.title = title
        self.ville = ville
        self.status = status

    @staticmethod
    def from_dict(obj: Any) -> Cartographie:
        assert isinstance(obj, dict)
        adresse = from_str(obj, "adresse")
        code_postal = from_int(obj, "codePostal")
        coordonnees = from_obj(Coordonnees.from_dict, obj, "coordonnees")
        date_created = from_datetime(obj, "date_created")
        date_updated = from_datetime(obj, "date_updated")
        cartographie_id = from_str(obj, "id")
        latitude = from_float(obj, "latitude")
        longitude = from_float(obj, "longitude")
        title = from_str(obj, "title")
        ville = from_str(obj, "ville")
        status = from_str(obj, "status")
        return Cartographie(
            adresse,
            code_postal,
            coordonnees,
            date_created,
            date_updated,
            cartographie_id,
            latitude,
            longitude,
            title,
            ville,
            status,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.adresse is not None:
            result["adresse"] = self.adresse
        if self.code_postal is not None:
            result["codePostal"] = str(self.code_postal)
        if self.coordonnees is not None:
            result["coordonnees"] = self.coordonnees.to_dict()
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.cartographie_id is not None:
            result["id"] = self.cartographie_id
        if self.latitude is not None:
            result["latitude"] = self.latitude
        if self.longitude is not None:
            result["longitude"] = self.longitude
        if self.title is not None:
            result["title"] = self.title
        if self.ville is not None:
            result["ville"] = self.ville
        if self.status is not None:
            result["status"] = self.status
        return result
