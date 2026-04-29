"""Response model for a single entraineur from items/ffbbserver_entraineurs."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class GetEntraineurResponse(BaseModel):
    """Represents an entraîner returned by the REST API.

    This model wraps the data from ``items/ffbbserver_entraineurs/{id}``.
    Fields are optional to accommodate partial field queries.
    """

    id: int | None = None
    nom: str | None = None
    prenom: str | None = None
    licence: str | None = None
    niveau_formation: str | None = Field(default=None, alias="niveauFormation")
    id_organisme: Any | None = Field(default=None, alias="idOrganisme")
    actif: bool | None = None
    date_updated: str | None = Field(default=None, alias="date_updated")

    model_config = {"populate_by_name": True, "extra": "allow"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GetEntraineurResponse":
        return cls.model_validate(data)
