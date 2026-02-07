from __future__ import annotations

from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_bool,
    from_datetime,
    from_enum,
    from_str,
)
from .code import Code

# from .multi_search_result_tournois import Libelle


class NatureSol:
    code: Code | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    id: str | None = None
    libelle: str | None = None
    terrain: bool | None = None

    def __init__(
        self,
        code: Code | None = None,
        date_created: datetime | None = None,
        date_updated: datetime | None = None,
        id: str | None = None,
        libelle: str | None = None,
        terrain: bool | None = None,
    ) -> None:
        self.code = code
        self.date_created = date_created
        self.date_updated = date_updated
        self.id = id
        self.libelle = libelle
        self.terrain = terrain

    @staticmethod
    def from_dict(obj: Any) -> NatureSol:
        assert isinstance(obj, dict)
        code = from_enum(Code, obj, "code")
        date_created = from_datetime(obj, "date_created")
        date_updated = from_datetime(obj, "date_updated")
        id = from_str(obj, "id")
        libelle = from_str(obj, "libelle")
        terrain = from_bool(obj, "terrain")
        return NatureSol(code, date_created, date_updated, id, libelle, terrain)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = self.code.value
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.id is not None:
            result["id"] = self.id
        if self.libelle is not None:
            result["libelle"] = self.libelle
        if self.terrain is not None:
            result["terrain"] = str(self.terrain).lower()
        return result
