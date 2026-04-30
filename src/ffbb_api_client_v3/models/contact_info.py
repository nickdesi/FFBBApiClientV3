from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ContactInfo:
    """Compact contact information used by V3 composite helpers.

    Fields are intentionally simple (no enums) to keep the model lightweight
    and avoid tight coupling with Directus-specific enums.
    """

    nom: str | None = None
    prenom: str | None = None
    email: str | None = None
    telephone: str | None = None
    role: str | None = None
