from __future__ import annotations

from typing import Any
from uuid import UUID

from ..utils.converter_utils import from_str, from_uuid


class IDOrganismeEquipe1Logo:
    id: UUID | None = None
    gradient_color: str | None = None

    def __init__(self, id: UUID | None, gradient_color: str | None) -> None:
        self.id = id
        self.gradient_color = gradient_color

    @staticmethod
    def from_dict(obj: Any) -> IDOrganismeEquipe1Logo:
        assert isinstance(obj, dict)
        id = from_uuid(obj, "id")
        gradient_color = from_str(obj, "gradient_color")
        return IDOrganismeEquipe1Logo(id, gradient_color)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = str(self.id)
        if self.gradient_color is not None:
            result["gradient_color"] = self.gradient_color
        return result
