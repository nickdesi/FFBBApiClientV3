from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from .contact_info import ContactInfo
from .get_organisme_response import GetOrganismeResponse


def _normalize_phone(raw: str | None) -> str | None:
    if not raw:
        return None
    return str(raw).strip()


def _sanitize_name(name: str | None) -> str | None:
    return name.strip().title() if name else None


@dataclass
class ClubContacts:
    """Contacts for a club: extracted club-level contact + members (dirigeants).

    `organisme` is kept for callers who want the original source object.
    """

    organisme: GetOrganismeResponse
    club_contact: ContactInfo | None
    membres: list[ContactInfo] = field(default_factory=list)


def extract_club_info(organisme: GetOrganismeResponse) -> ContactInfo | None:
    """Extract club-level contact info (phone / mail) from an organisme."""
    phone = _normalize_phone(getattr(organisme, "telephone", None))
    email = getattr(organisme, "mail", None) or None
    if not phone and not email:
        return None
    return ContactInfo(
        nom=getattr(organisme, "nom", None),
        prenom=None,
        telephone=phone,
        email=email,
        role="club",
    )


def extract_membres_contacts(organisme: GetOrganismeResponse) -> list[ContactInfo]:
    """Extract contacts from the `membres` list on an organisme.

    This is defensive: it accepts multiple possible attribute names used by
    different model versions (camelCase or snake_case) and falls back to
    reasonable defaults.
    """
    contacts: list[ContactInfo] = []
    membres: Iterable = getattr(organisme, "membres", []) or []
    for membre in membres:
        phone = _normalize_phone(
            getattr(membre, "telephonePortable", None)
            or getattr(membre, "telephone_portable", None)
            or getattr(membre, "telephoneFixe", None)
            or getattr(membre, "telephone_fixe", None)
        )
        email = getattr(membre, "mail", None) or None
        if not phone and not email:
            continue
        contacts.append(
            ContactInfo(
                nom=_sanitize_name(getattr(membre, "nom", None)),
                prenom=_sanitize_name(getattr(membre, "prenom", None)),
                telephone=phone,
                email=email,
                role=getattr(membre, "codeFonction", None)
                or getattr(membre, "code_fonction", None)
                or "membre",
            )
        )
    return contacts
