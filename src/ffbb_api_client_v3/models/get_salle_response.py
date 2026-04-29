from dataclasses import dataclass


@dataclass
class GetSalleResponse:
    id: str
    numero: str | None = None
    libelle: str | None = None
    adresse: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "GetSalleResponse | None":
        if not data or not isinstance(data, dict):
            return None
        return cls(
            id=str(data.get("id", "")),
            numero=data.get("numero"),
            libelle=data.get("libelle"),
            adresse=data.get("adresse"),
        )
