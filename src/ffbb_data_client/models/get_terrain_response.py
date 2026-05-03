from dataclasses import dataclass


@dataclass
class GetTerrainResponse:
    id: str
    nom: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "GetTerrainResponse | None":
        if not data or not isinstance(data, dict):
            return None
        return cls(
            id=str(data.get("id", "")),
            nom=data.get("nom"),
        )
