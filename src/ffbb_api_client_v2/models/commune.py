from __future__ import annotations

from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_datetime,
    from_int,
    from_str,
)


class Commune:
    code_insee: str | None = None
    code_postal: int | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    commune_id: int | None = None
    libelle: str | None = None
    departement: str | None = None

    def __init__(
        self,
        code_insee: str | None,
        code_postal: int | None,
        date_created: datetime | None,
        date_updated: datetime | None,
        id: int | None,
        libelle: str | None,
        departement: str | None,
    ):
        self.code_insee = code_insee
        self.code_postal = code_postal
        self.date_created = date_created
        self.date_updated = date_updated
        self.commune_id = id
        self.libelle = libelle
        self.lower_libelle = libelle.lower() if libelle else None

        self.departement = departement
        self.lower_departement = departement.lower() if departement else None

    @staticmethod
    def from_dict(obj: Any) -> Commune:
        assert isinstance(obj, dict)
        code_insee = from_str(obj, "codeInsee")
        code_postal = from_int(obj, "codePostal")
        date_created = from_datetime(obj, "date_created")
        date_updated = from_datetime(obj, "date_updated")
        commune_id = from_int(obj, "id")
        libelle = from_str(obj, "libelle")
        departement = from_str(obj, "departement")
        return Commune(
            code_insee,
            code_postal,
            date_created,
            date_updated,
            commune_id,
            libelle,
            departement,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code_insee is not None:
            result["codeInsee"] = self.code_insee
        if self.code_postal is not None:
            result["codePostal"] = str(self.code_postal)
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.commune_id is not None:
            result["id"] = str(self.commune_id)
        if self.libelle is not None:
            result["libelle"] = self.libelle
        if self.departement is not None:
            result["departement"] = self.departement
        return result
