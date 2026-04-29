from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class GetRencontreResponse:
    id: str
    numero: str | None = None
    date_rencontre: datetime | None = None
    resultatEquipe1: str | None = None
    resultatEquipe2: str | None = None
    joue: int = 0
    nomEquipe1: str | None = None
    nomEquipe2: str | None = None
    idPoule: str | None = None
    competitionId: Any | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "GetRencontreResponse | None":
        if not data or not isinstance(data, dict):
            return None
        date_str = data.get("date_rencontre")
        date = None
        if date_str:
            try:
                date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                pass
        return cls(
            id=str(data.get("id", "")),
            numero=data.get("numero"),
            date_rencontre=date,
            resultatEquipe1=data.get("resultatEquipe1"),
            resultatEquipe2=data.get("resultatEquipe2"),
            joue=int(data.get("joue", 0)),
            nomEquipe1=data.get("nomEquipe1"),
            nomEquipe2=data.get("nomEquipe2"),
            idPoule=data.get("idPoule"),
            competitionId=data.get("competitionId"),
        )
