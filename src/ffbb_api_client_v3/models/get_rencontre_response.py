"""Response model for a single rencontre from items/ffbbserver_rencontres."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class GetRencontreResponse(BaseModel):
    """Represents a single rencontre returned by the REST API.

    This model wraps the data from ``items/ffbbserver_rencontres/{id}``.
    Fields are marked optional with ``None`` default to handle partial
    field selection via ``fields[]`` query parameters.
    """

    id: int | None = None
    date: str | None = None
    heure: str | None = None
    salle: Any | None = None
    equipe1: Any | None = None
    equipe2: Any | None = None
    score_equipe1: int | None = None
    score_equipe2: int | None = None
    statut: str | None = None
    id_poule: Any | None = Field(default=None, alias="idPoule")
    competition_id: Any | None = Field(default=None, alias="competitionId")
    niveau: Any | None = None
    numero_journee: int | None = Field(default=None, alias="numeroJournee")
    date_updated: str | None = Field(default=None, alias="date_updated")

    model_config = {"populate_by_name": True, "extra": "allow"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GetRencontreResponse":
        return cls.model_validate(data)
