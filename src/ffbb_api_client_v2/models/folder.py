from __future__ import annotations

from typing import Any
from uuid import UUID

from ..utils.converter_utils import (
    from_none,
    from_str,
    from_uuid,
)


class Folder:
    id: UUID | None = None
    name: str | None = None
    parent: None

    def __init__(
        self,
        id: UUID | None = None,
        name: str | None = None,
        parent: None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.parent = parent

    @staticmethod
    def from_dict(obj: Any) -> Folder:
        assert isinstance(obj, dict)
        id = from_uuid(obj, "id")
        name = from_str(obj, "name")
        parent = from_none(obj.get("parent"))
        return Folder(id, name, parent)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = str(self.id)
        if self.name is not None:
            result["name"] = self.name
        if self.parent is not None:
            result["parent"] = from_none(self.parent)
        return result
