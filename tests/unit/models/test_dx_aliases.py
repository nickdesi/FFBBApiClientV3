"""Tests for DX aliases and flattened properties in models."""
import pytest
from datetime import datetime
from ffbb_api_client_v3.models.organismes_hit import OrganismesHit
from ffbb_api_client_v3.models.competitions_hit import CompetitionsHit
from ffbb_api_client_v3.models.salles_hit import SallesHit
from ffbb_api_client_v3.models.rencontres_hit import RencontresHit
from ffbb_api_client_v3.models.get_organisme_response import GetOrganismeResponse
from ffbb_api_client_v3.models.poule_rencontre_item_model import PouleRencontreItemModel

def test_organismes_hit_name_alias():
    """OrganismesHit.name should alias to .nom."""
    hit = OrganismesHit(id="1", nom="Club Test")
    assert hit.name == "Club Test"

def test_competitions_hit_name_alias():
    """CompetitionsHit.name should alias to .nom."""
    hit = CompetitionsHit(id="1", nom="Competition Test")
    assert hit.name == "Competition Test"

def test_salles_hit_name_alias():
    """SallesHit.name should alias to .libelle."""
    hit = SallesHit(id="1", libelle="Salle Test")
    assert hit.name == "Salle Test"

def test_rencontres_hit_aliases():
    """RencontresHit should have name, team1_name and team2_name aliases."""
    hit = RencontresHit(id="1", nom_equipe1="Team A", nom_equipe2="Team B")
    assert hit.team1_name == "Team A"
    assert hit.team2_name == "Team B"
    assert hit.name == "Team A vs Team B"

def test_engagements_convenience_properties():
    """EngagementsitemModel should have flattened properties."""
    # Setup nested objects
    class IdPoule:
        id = "p1"
    class IdCompetition:
        nom = "Comp Test"
    
    engagement = GetOrganismeResponse.EngagementsitemModel(
        id="eng1",
        idPoule=IdPoule(),
        idCompetition=IdCompetition(),
        numeroEquipe="1"
    )
    
    assert engagement.poule_id == "p1"
    assert engagement.competition_nom == "Comp Test"
    assert engagement.numero_equipe == "1"

def test_poule_rencontre_aliases():
    """PouleRencontreItemModel should have snake_case aliases."""
    item = PouleRencontreItemModel(
        id="1",
        numero="M123",
        numeroJournee="J1",
        idPoule="P456",
        competitionId="C789",
        resultatEquipe1="80",
        resultatEquipe2="75",
        joue=1,
        nomEquipe1="Home Team",
        nomEquipe2="Away Team",
        date_rencontre=datetime.now()
    )
    
    assert item.team1_name == "Home Team"
    assert item.equipe_locale == "Home Team"
    assert item.team2_name == "Away Team"
    assert item.equipe_visiteuse == "Away Team"
    assert item.score1 == "80"
    assert item.score2 == "75"
    assert item.poule_id == "P456"
    assert item.match_number == "M123"
    assert item.round_number == "J1"
    assert item.is_played is True
