from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_obj
from .purple_logo import PurpleLogo


@dataclass
class CompetitionOrigineTypeCompetitionGenerique:
    logo: PurpleLogo | None = None

    @staticmethod
    def from_dict(obj: Any) -> CompetitionOrigineTypeCompetitionGenerique:
        assert isinstance(obj, dict)
        logo = from_obj(PurpleLogo.from_dict, obj, "logo")
        return CompetitionOrigineTypeCompetitionGenerique(logo=logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        return result
