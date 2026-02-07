from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_int


class CompetitionIDSexe:
    feminine: int | None = None
    masculine: int | None = None
    mixed: int | None = None

    def __init__(
        self, feminine: int | None, masculine: int | None, mixed: int | None
    ) -> None:
        self.feminine = feminine
        self.masculine = masculine
        self.mixed = mixed

    @staticmethod
    def from_dict(obj: Any) -> CompetitionIDSexe:
        assert isinstance(obj, dict)
        feminine = from_int(obj, "Féminin")
        masculine = from_int(obj, "Masculin")
        mixed = from_int(obj, "Mixte")
        return CompetitionIDSexe(feminine, masculine, mixed)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.feminine is not None:
            result["Féminin"] = self.feminine
        if self.masculine is not None:
            result["Masculin"] = self.masculine
        if self.mixed is not None:
            result["Mixte"] = self.mixed
        return result
