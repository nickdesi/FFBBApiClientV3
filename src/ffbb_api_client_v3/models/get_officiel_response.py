"""Response model for a single officiel from items/ffbbserver_officiels."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class GetOfficielResponse(BaseModel):
    """Represents an officiel (arbitre, etc.) returned by the REST API.

    This model wraps the data from ``items/ffbbserver_officiels/{id}``.
    Fields are optional to accommodate partial field queries.
    """

    id: int | None = None
    nom: str | None = None
    prenom: str | None = None
    licence: str | None = None
    type_officiel: str | None = Field(default=None, alias="typeOfficiel")
    id_organisme: Any | None = Field(default=None, alias="idOrganisme")
    actif: bool | None = None
    date_updated: str | None = Field(default=None, alias="date_updated")

    model_config = {"populate_by_name": True, "extra": "allow"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GetOfficielResponse":
        return cls.model_validate(data)
