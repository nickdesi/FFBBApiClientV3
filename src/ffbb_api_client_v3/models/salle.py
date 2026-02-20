from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..utils.converter_utils import from_obj, from_str
from .cartographie import Cartographie


@dataclass
class Salle:
    id: str | None = None
    libelle: str | None = None
    adresse: str | None = None
    adresse_complement: str | None = None
    cartographie: Cartographie | None = None
    lower_libelle: str | None = field(init=False, default=None, repr=False)
    lower_adresse: str | None = field(init=False, default=None, repr=False)
    lower_adresse_complement: str | None = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self.lower_libelle = self.libelle.lower() if self.libelle else None
        self.lower_adresse = self.adresse.lower() if self.adresse else None
        self.lower_adresse_complement = (
            self.adresse_complement.lower() if self.adresse_complement else None
        )

    @staticmethod
    def from_dict(obj: Any) -> Salle:
        assert isinstance(obj, dict)
        id = from_str(obj, "id")
        libelle = from_str(obj, "libelle")
        adresse = from_str(obj, "adresse")
        adresse_complement = from_str(obj, "adresseComplement")
        cartographie = from_obj(Cartographie.from_dict, obj, "cartographie")
        return Salle(
            id=id,
            libelle=libelle,
            adresse=adresse,
            adresse_complement=adresse_complement,
            cartographie=cartographie,
        )

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
