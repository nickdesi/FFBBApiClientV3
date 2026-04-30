from __future__ import annotations

from dataclasses import dataclass

from .contact_info import ContactInfo
from .get_engagement_response import GetEngagementResponse
from .get_entraineur_response import GetEntraineurResponse


def _normalize_phone(raw: str | None) -> str | None:
    if not raw:
        return None
    return str(raw).strip()


def _sanitize_name(name: str | None) -> str | None:
    return name.strip().title() if name else None


@dataclass
class EngagementContacts:
    """Contacts for an engagement (team): correspondant + coaches."""

    engagement: GetEngagementResponse
    correspondant: ContactInfo | None
    entraineur: ContactInfo | None
    entraineur_adjoint: ContactInfo | None


def extract_correspondant(engagement: GetEngagementResponse) -> ContactInfo | None:
    """Extract correspondant contact from an engagement.

    This is defensive: the engagement model in V3 may or may not include
    correspondent phone/email fields. We try common attribute names and return
    None if nothing usable is found.
    """
    phone = _normalize_phone(
        getattr(engagement, "telephonePortableCorrespondantEquipe", None)
        or getattr(engagement, "telephone_portable_correspondant_equipe", None)
        or getattr(engagement, "telephoneFixeCorrespondantEquipe", None)
        or getattr(engagement, "telephone_fixe_correspondant_equipe", None)
        or getattr(engagement, "telephone", None)
    )
    email = (
        getattr(engagement, "emailCorrespondantEquipe", None)
        or getattr(engagement, "email_correspondant_equipe", None)
        or getattr(engagement, "email", None)
    )
    if not phone and not email:
        return None
    return ContactInfo(
        nom=_sanitize_name(
            getattr(engagement, "nomCorrespondantEquipe", None)
            or getattr(engagement, "nom", None)
        ),
        prenom=_sanitize_name(
            getattr(engagement, "prenomCorrespondantEquipe", None)
            or getattr(engagement, "prenom", None)
        ),
        telephone=phone,
        email=email,
        role="correspondant",
    )


def extract_entraineur_contact(
    entraineur: GetEntraineurResponse | None, titre: str | None
) -> ContactInfo | None:
    """Extract contact info from an entraineur object.

    If phone/email are missing we still return a name-only ContactInfo when
    at least a name is present so callers can display a best-effort contact.
    """
    if not entraineur:
        return None
    phone = _normalize_phone(
        getattr(entraineur, "telephonePortable", None)
        or getattr(entraineur, "telephone_portable", None)
        or getattr(entraineur, "telephoneDomicile", None)
        or getattr(entraineur, "telephone_travail", None)
        or getattr(entraineur, "telephone", None)
    )
    email = getattr(entraineur, "email", None) or None
    if (
        not phone
        and not email
        and not getattr(entraineur, "nom", None)
        and not getattr(entraineur, "prenom", None)
    ):
        return None
    return ContactInfo(
        nom=_sanitize_name(getattr(entraineur, "nom", None)),
        prenom=_sanitize_name(getattr(entraineur, "prenom", None)),
        telephone=phone,
        email=email,
        role=titre,
    )
