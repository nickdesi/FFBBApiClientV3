from dataclasses import dataclass


@dataclass
class GetPratiqueResponse:
    id: str
    label: str | None = None
    type: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "GetPratiqueResponse | None":
        if not data or not isinstance(data, dict):
            return None
        return cls(
            id=str(data.get("id", "")),
            label=data.get("label"),
            type=data.get("type"),
        )
