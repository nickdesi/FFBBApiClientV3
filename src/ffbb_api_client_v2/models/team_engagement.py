from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_obj, from_str
from .logo import Logo


@dataclass
class TeamEngagement:
    nom_officiel: str | None = None
    nom_usuel: str | None = None
    code_abrege: str | None = None
    logo: Logo | None = None

    def __init__(
        self,
        nom_officiel: str | None,
        nom_usuel: str | None,
        code_abrege: str | None,
        logo: Logo | None,
    ) -> None:
        self.nom_officiel = nom_officiel
        self.nom_usuel = nom_usuel
        self.code_abrege = code_abrege
        self.logo = logo

    @staticmethod
    def from_dict(obj: Any) -> TeamEngagement:
        """
        Convert a dictionary object to a TeamEngagement instance.

        Args:
            obj (Any): The dictionary object to convert.

        Returns:
            TeamEngagement: The converted TeamEngagement instance.
        """
        assert isinstance(obj, dict)
        nom_officiel = from_str(obj, "nomOfficiel")
        nom_usuel = from_str(obj, "nomUsuel")
        code_abrege = from_str(obj, "codeAbrege")
        logo = from_obj(Logo.from_dict, obj, "logo")
        return TeamEngagement(nom_officiel, nom_usuel, code_abrege, logo)

    def to_dict(self) -> dict:
        """
        Convert the TeamEngagement instance to a dictionary object.

        Returns:
            dict: The converted dictionary object.
        """
        result: dict = {}
        if self.nom_officiel is not None:
            result["nomOfficiel"] = self.nom_officiel
        if self.nom_usuel is not None:
            result["nomUsuel"] = self.nom_usuel
        if self.code_abrege is not None:
            result["codeAbrege"] = self.code_abrege
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        return result
