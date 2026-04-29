from dataclasses import dataclass


@dataclass
class GetCommuneResponse:
    id: str
    libelle: str | None = None
    codePostal: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "GetCommuneResponse | None":
        if not data or not isinstance(data, dict):
            return None
        return cls(
            id=str(data.get("id", "")),
            libelle=data.get("libelle"),
            codePostal=data.get("codePostal"),
        )
