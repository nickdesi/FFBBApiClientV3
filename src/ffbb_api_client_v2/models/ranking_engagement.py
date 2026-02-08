from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RankingEngagement:
    """Modèle pour l'engagement d'une équipe dans un classement."""

    id: str
    nom: str
    nom_usuel: str | None = None
    code_abrege: str | None = None
    numero_equ: str | None = None
    numero_equipe: str | None = None
    logo_id: str | None = None
    logo_gradient: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> RankingEngagement | None:
        """Convert dictionary to RankingEngagement instance."""
        if not data:
            return None

        # Handle logo data
        logo_data = data.get("logo", {})
        logo_id = logo_data.get("id") if isinstance(logo_data, dict) else None
        logo_gradient = (
            logo_data.get("gradient_color") if isinstance(logo_data, dict) else None
        )

        return cls(
            id=str(data.get("id", "")),
            nom=str(data.get("nom", "")),
            nom_usuel=data.get("nomUsuel"),
            code_abrege=data.get("codeAbrege"),
            numero_equ=data.get("numeroEqu"),
            numero_equipe=data.get("numeroEquipe"),
            logo_id=str(logo_id) if logo_id else None,
            logo_gradient=str(logo_gradient) if logo_gradient else None,
        )
