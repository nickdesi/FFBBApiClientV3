from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_obj, from_str
from .cartographie import Cartographie


class Salle:
    id: str | None = None
    libelle: str | None = None
    adresse: str | None = None
    adresse_complement: str | None = None
    cartographie: Cartographie | None = None

    def __init__(
        self,
        id: str | None,
        libelle: str | None,
        adresse: str | None,
        adresse_complement: str | None,
        cartographie: Cartographie | None,
    ) -> None:
        self.id = id
        self.libelle = libelle
        self.lower_libelle = libelle.lower() if libelle else None

        self.adresse = adresse
        self.lower_adresse = adresse.lower() if adresse else None

        self.adresse_complement = adresse_complement
        self.lower_adresse_complement = (
            adresse_complement.lower() if adresse_complement else None
        )
        self.cartographie = cartographie

    @staticmethod
    def from_dict(obj: Any) -> Salle:
        assert isinstance(obj, dict)
        id = from_str(obj, "id")
        libelle = from_str(obj, "libelle")
        adresse = from_str(obj, "adresse")
        adresse_complement = from_str(obj, "adresseComplement")
        cartographie = from_obj(Cartographie.from_dict, obj, "cartographie")
        return Salle(id, libelle, adresse, adresse_complement, cartographie)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.libelle is not None:
            result["libelle"] = self.libelle
        if self.adresse is not None:
            result["adresse"] = self.adresse
        if self.adresse_complement is not None:
            result["adresseComplement"] = self.adresse_complement
        if self.cartographie is not None:
            result["cartographie"] = self.cartographie.to_dict()
        return result
