from dataclasses import dataclass
from typing import Any


@dataclass
class GetEngagementResponse:
    id: str
    numeroEquipe: str | None = None
    idPoule: Any | None = None
    idCompetition: Any | None = None
    idOrganisme: Any | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "GetEngagementResponse | None":
        if not data or not isinstance(data, dict):
            return None
        return cls(
            id=str(data.get("id", "")),
            numeroEquipe=data.get("numeroEquipe"),
            idPoule=data.get("idPoule"),
            idCompetition=data.get("idCompetition"),
            idOrganisme=data.get("idOrganisme"),
        )
