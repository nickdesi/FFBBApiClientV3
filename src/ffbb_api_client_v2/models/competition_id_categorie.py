from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_int, from_str


class CompetitionIDCategorie:
    code: str | None = None
    libelle: str | None = None
    ordre: int | None = None

    def __init__(
        self, code: str | None, libelle: str | None, ordre: int | None
    ) -> None:
        self.code = code
        self.libelle = libelle
        self.ordre = ordre

    @staticmethod
    def from_dict(obj: Any) -> CompetitionIDCategorie:
        assert isinstance(obj, dict)
        code = from_str(obj, "code")
        libelle = from_str(obj, "libelle")
        ordre = from_int(obj, "ordre")
        return CompetitionIDCategorie(code, libelle, ordre)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = self.code
        if self.libelle is not None:
            result["libelle"] = self.libelle
        if self.ordre is not None:
            result["ordre"] = self.ordre
        return result
