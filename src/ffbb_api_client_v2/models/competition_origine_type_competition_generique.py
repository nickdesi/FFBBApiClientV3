from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_obj
from .purple_logo import PurpleLogo


class CompetitionOrigineTypeCompetitionGenerique:
    logo: PurpleLogo | None = None

    def __init__(self, logo: PurpleLogo | None) -> None:
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> CompetitionOrigineTypeCompetitionGenerique:
        assert isinstance(obj, dict)
        logo = from_obj(PurpleLogo.from_dict, obj, "logo")
        return CompetitionOrigineTypeCompetitionGenerique(logo)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        return result
