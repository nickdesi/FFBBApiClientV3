"""Backward-compatibility re-export shim for niveau module."""

from .categorie_type import CategorieType
from .niveau_extractor import NiveauExtractor, get_niveau_from_idcompetition
from .niveau_info import NiveauInfo
from .niveau_type import NiveauType

__all__ = [
    "CategorieType",
    "NiveauExtractor",
    "NiveauInfo",
    "NiveauType",
    "get_niveau_from_idcompetition",
]
