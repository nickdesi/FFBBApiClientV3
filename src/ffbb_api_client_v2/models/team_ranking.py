from __future__ import annotations

from dataclasses import dataclass

from .ranking_engagement import RankingEngagement


@dataclass
class TeamRanking:
    """Modèle pour un classement d'équipe."""

    # Required fields first
    id: str
    id_engagement: RankingEngagement | None
    position: int
    points: int
    match_joues: int
    gagnes: int
    perdus: int
    nombre_forfaits: int
    paniers_marques: int
    paniers_encaisses: int
    difference: int
    quotient: float
    # Optional fields with defaults
    nuls: int | None = None
    nombre_defauts: int | None = None
    point_initiaux: int | None = None
    penalites_arbitrage: int | None = None
    penalites_entraineur: int | None = None
    penalites_diverses: int | None = None
    hors_classement: bool | None = None
    # Relation fields
    organisme_id: str | None = None
    organisme_nom: str | None = None
    organisme_logo_id: str | None = None
    organisme_nom_simple: str | None = None
    id_competition: str | None = None
    id_poule: str | None = None
    id_poule_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> TeamRanking | None:
        """Convert dictionary to TeamRanking instance."""
        if not data:
            return None

        # Handle case where data is not a dictionary
        if not isinstance(data, dict):
            return None

        id_engagement_data = data.get("idEngagement", {})
        id_engagement = (
            RankingEngagement.from_dict(id_engagement_data)
            if id_engagement_data
            else None
        )

        # Handle organisme data
        organisme_data = data.get("organisme", {})
        organisme_id = (
            organisme_data.get("id") if isinstance(organisme_data, dict) else None
        )
        organisme_nom = (
            organisme_data.get("nom") if isinstance(organisme_data, dict) else None
        )
        organisme_nom_simple = (
            organisme_data.get("nom_simple")
            if isinstance(organisme_data, dict)
            else None
        )

        # Handle organisme logo
        organisme_logo_data = (
            organisme_data.get("logo", {}) if isinstance(organisme_data, dict) else {}
        )
        organisme_logo_id = (
            organisme_logo_data.get("id")
            if isinstance(organisme_logo_data, dict)
            else None
        )

        # Handle idPoule data
        id_poule_data = data.get("idPoule", {})
        id_poule_id = (
            id_poule_data.get("id") if isinstance(id_poule_data, dict) else None
        )

        return cls(
            id=str(data.get("id", "")),
            id_engagement=id_engagement,
            position=int(data.get("position", 0)),
            points=int(data.get("points", 0)),
            match_joues=int(data.get("matchJoues", 0)),
            gagnes=int(data.get("gagnes", 0)),
            perdus=int(data.get("perdus", 0)),
            nuls=(
                int(nuls_val) if (nuls_val := data.get("nuls")) is not None else None
            ),
            nombre_forfaits=int(data.get("nombreForfaits", 0)),
            nombre_defauts=(
                int(defauts_val)
                if (defauts_val := data.get("nombreDefauts")) is not None
                else None
            ),
            paniers_marques=int(data.get("paniersMarques", 0)),
            paniers_encaisses=int(data.get("paniersEncaisses", 0)),
            difference=int(data.get("difference", 0)),
            quotient=float(data.get("quotient", 0.0)),
            point_initiaux=(
                int(initiaux_val)
                if (initiaux_val := data.get("pointInitiaux")) is not None
                else None
            ),
            penalites_arbitrage=(
                int(arb_val)
                if (arb_val := data.get("penalitesArbitrage")) is not None
                else None
            ),
            penalites_entraineur=(
                int(entr_val)
                if (entr_val := data.get("penalitesEntraineur")) is not None
                else None
            ),
            penalites_diverses=(
                int(div_val)
                if (div_val := data.get("penalitesDiverses")) is not None
                else None
            ),
            hors_classement=(
                bool(data.get("horsClassement"))
                if data.get("horsClassement") is not None
                else None
            ),
            organisme_id=str(organisme_id) if organisme_id else None,
            organisme_nom=str(organisme_nom) if organisme_nom else None,
            organisme_logo_id=str(organisme_logo_id) if organisme_logo_id else None,
            organisme_nom_simple=(
                str(organisme_nom_simple) if organisme_nom_simple else None
            ),
            id_competition=(
                str(data.get("idCompetition")) if data.get("idCompetition") else None
            ),
            id_poule=str(data.get("idPoule")) if data.get("idPoule") else None,
            id_poule_id=str(id_poule_id) if id_poule_id else None,
        )
