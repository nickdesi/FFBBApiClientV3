from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_int


class CompetitionIDTypeCompetition:
    championnat: int | None = None
    coupe: int | None = None

    def __init__(self, championnat: int | None, coupe: int | None) -> None:
        self.championnat = championnat
        self.coupe = coupe

    @staticmethod
    def from_dict(obj: Any) -> CompetitionIDTypeCompetition:
        assert isinstance(obj, dict)
        championnat = from_int(obj, "Championnat")
        coupe = from_int(obj, "Coupe")
        return CompetitionIDTypeCompetition(championnat, coupe)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.championnat is not None:
            result["Championnat"] = self.championnat
        if self.coupe is not None:
            result["Coupe"] = self.coupe
        return result
