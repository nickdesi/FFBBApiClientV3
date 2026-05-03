from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class PouleRencontreItemModel:
    id: str
    numero: str
    numeroJournee: str
    idPoule: str
    competitionId: str
    resultatEquipe1: str
    resultatEquipe2: str
    joue: int
    nomEquipe1: str
    nomEquipe2: str
    date_rencontre: datetime

    @property
    def team1_name(self) -> str:
        """Alias for nomEquipe1."""
        return self.nomEquipe1

    @property
    def equipe_locale(self) -> str:
        """Alias for nomEquipe1."""
        return self.nomEquipe1

    @property
    def team2_name(self) -> str:
        """Alias for nomEquipe2."""
        return self.nomEquipe2

    @property
    def equipe_visiteuse(self) -> str:
        """Alias for nomEquipe2."""
        return self.nomEquipe2

    @property
    def score1(self) -> str:
        """Alias for resultatEquipe1."""
        return self.resultatEquipe1

    @property
    def score2(self) -> str:
        """Alias for resultatEquipe2."""
        return self.resultatEquipe2

    @property
    def poule_id(self) -> str:
        """Alias for idPoule."""
        return self.idPoule

    @property
    def match_number(self) -> str:
        """Alias for numero."""
        return self.numero

    @property
    def round_number(self) -> str:
        """Alias for numeroJournee."""
        return self.numeroJournee

    @property
    def is_played(self) -> bool:
        """Returns True if the match has been played."""
        return bool(self.joue)
