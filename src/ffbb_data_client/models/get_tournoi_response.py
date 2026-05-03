from dataclasses import dataclass


@dataclass
class GetTournoiResponse:
    id: str
    libelle: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "GetTournoiResponse | None":
        if not data or not isinstance(data, dict):
            return None
        return cls(
            id=str(data.get("id", "")),
            libelle=data.get("libelle"),
        )
