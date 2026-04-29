from dataclasses import dataclass
from typing import Any


@dataclass
class GetFormationResponse:
    id: str
    theme: str | None = None
    type: str | None = None
    domain: str | None = None
    mode: str | None = None
    place: str | None = None
    date_start: str | None = None
    date_end: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "GetFormationResponse | None":
        if not data or not isinstance(data, dict):
            return None
        return cls(
            id=str(data.get("id", "")),
            theme=data.get("theme"),
            type=data.get("type"),
            domain=data.get("domain"),
            mode=data.get("mode"),
            place=data.get("place"),
            date_start=data.get("date_start"),
            date_end=data.get("date_end"),
        )
