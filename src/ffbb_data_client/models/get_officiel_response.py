from dataclasses import dataclass


@dataclass
class GetOfficielResponse:
    id: str
    nom: str | None = None
    prenom: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "GetOfficielResponse | None":
        if not data or not isinstance(data, dict):
            return None
        return cls(
            id=str(data.get("id", "")),
            nom=data.get("nom"),
            prenom=data.get("prenom"),
        )
