"""Tests to bring remaining modules to >= 90% coverage.

Targets:
- Enums at 0% (terrains_name, terrains_storage, tournois_libelle)
- FacetStats / FacetDistribution subclasses (78-91%)
- Models with uncovered to_dict branches
- converter_utils edge cases (from_officiels_list, from_str exception path)
"""

from __future__ import annotations

import logging

import pytest

# ===========================================================================
# Groupe 1 : Enums at 0%
# ===========================================================================


class TestTerrainsNameEnum:
    def test_tournois_value(self):
        from ffbb_api_client_v2.models.terrains_name import Name

        assert Name.TOURNOIS.value == "Tournois"

    def test_from_value(self):
        from ffbb_api_client_v2.models.terrains_name import Name

        assert Name("Tournois") is Name.TOURNOIS


class TestTerrainsStorageEnum:
    def test_minio_value(self):
        from ffbb_api_client_v2.models.terrains_storage import Storage

        assert Storage.MINIO.value == "minio"

    def test_from_value(self):
        from ffbb_api_client_v2.models.terrains_storage import Storage

        assert Storage("minio") is Storage.MINIO


class TestTournoisLibelleEnum:
    def test_bitume_value(self):
        from ffbb_api_client_v2.models.tournois_libelle import Libelle

        assert Libelle.BITUME.value == "BITUME"

    def test_beton_value(self):
        from ffbb_api_client_v2.models.tournois_libelle import Libelle

        assert Libelle.BÉTON.value == "Béton"

    def test_sol_synthetique_value(self):
        from ffbb_api_client_v2.models.tournois_libelle import Libelle

        assert Libelle.SOL_SYNTHÉTIQUE.value == "Sol synthétique"


# ===========================================================================
# Groupe 2 : FacetStats / FacetDistribution subclasses
# ===========================================================================


class TestCompetitionsFacetStats:
    def test_from_dict_returns_instance(self):
        from ffbb_api_client_v2.models.competitions_facet_stats import (
            CompetitionsFacetStats,
        )

        obj = CompetitionsFacetStats.from_dict({})
        assert isinstance(obj, CompetitionsFacetStats)

    def test_to_dict_returns_empty(self):
        from ffbb_api_client_v2.models.competitions_facet_stats import (
            CompetitionsFacetStats,
        )

        obj = CompetitionsFacetStats()
        assert obj.to_dict() == {}


class TestSallesFacetStats:
    def test_from_dict_returns_instance(self):
        from ffbb_api_client_v2.models.salles_facet_stats import SallesFacetStats

        obj = SallesFacetStats.from_dict({})
        assert isinstance(obj, SallesFacetStats)

    def test_to_dict_returns_empty(self):
        from ffbb_api_client_v2.models.salles_facet_stats import SallesFacetStats

        assert SallesFacetStats().to_dict() == {}


class TestSallesFacetDistribution:
    def test_from_dict_returns_instance(self):
        from ffbb_api_client_v2.models.salles_facet_distribution import (
            SallesFacetDistribution,
        )

        obj = SallesFacetDistribution.from_dict({})
        assert isinstance(obj, SallesFacetDistribution)

    def test_to_dict_returns_empty(self):
        from ffbb_api_client_v2.models.salles_facet_distribution import (
            SallesFacetDistribution,
        )

        assert SallesFacetDistribution().to_dict() == {}


class TestTerrainsFacetStats:
    def test_from_dict_returns_instance(self):
        from ffbb_api_client_v2.models.terrains_facet_stats import TerrainsFacetStats

        obj = TerrainsFacetStats.from_dict({})
        assert isinstance(obj, TerrainsFacetStats)

    def test_to_dict_returns_empty(self):
        from ffbb_api_client_v2.models.terrains_facet_stats import TerrainsFacetStats

        assert TerrainsFacetStats().to_dict() == {}


class TestRencontresFacetStats:
    def test_from_dict_returns_instance(self):
        from ffbb_api_client_v2.models.rencontres_facet_stats import (
            RencontresFacetStats,
        )

        obj = RencontresFacetStats.from_dict({})
        assert isinstance(obj, RencontresFacetStats)

    def test_to_dict_returns_empty(self):
        from ffbb_api_client_v2.models.rencontres_facet_stats import (
            RencontresFacetStats,
        )

        assert RencontresFacetStats().to_dict() == {}


class TestTournoisFacetStats:
    def test_from_dict_returns_instance(self):
        from ffbb_api_client_v2.models.tournois_facet_stats import TournoisFacetStats

        obj = TournoisFacetStats.from_dict({})
        assert isinstance(obj, TournoisFacetStats)

    def test_to_dict_returns_empty(self):
        from ffbb_api_client_v2.models.tournois_facet_stats import TournoisFacetStats

        assert TournoisFacetStats().to_dict() == {}


class TestRencontresFacetDistribution:
    """Cover from_dict({}) and to_dict() empty-branch paths."""

    def test_from_dict_empty(self):
        from ffbb_api_client_v2.models.rencontres_facet_distribution import (
            RencontresFacetDistribution,
        )

        obj = RencontresFacetDistribution.from_dict({})
        assert isinstance(obj, RencontresFacetDistribution)
        assert obj.competition_id_categorie_code is None
        assert obj.competition_id_sexe is None

    def test_to_dict_empty(self):
        from ffbb_api_client_v2.models.rencontres_facet_distribution import (
            RencontresFacetDistribution,
        )

        obj = RencontresFacetDistribution()
        assert obj.to_dict() == {}


class TestCompetitionsFacetDistribution:
    """Cover from_dict({}) and to_dict() empty-branch paths."""

    def test_from_dict_empty(self):
        from ffbb_api_client_v2.models.competitions_facet_distribution import (
            CompetitionsFacetDistribution,
        )

        obj = CompetitionsFacetDistribution.from_dict({})
        assert isinstance(obj, CompetitionsFacetDistribution)
        assert obj.competition_id_categorie_code is None

    def test_to_dict_empty(self):
        from ffbb_api_client_v2.models.competitions_facet_distribution import (
            CompetitionsFacetDistribution,
        )

        assert CompetitionsFacetDistribution().to_dict() == {}


class TestTerrainsFacetDistribution:
    """Cover from_dict({}) and to_dict() empty-branch paths."""

    def test_from_dict_empty(self):
        from ffbb_api_client_v2.models.terrains_facet_distribution import (
            TerrainsFacetDistribution,
        )

        obj = TerrainsFacetDistribution.from_dict({})
        assert isinstance(obj, TerrainsFacetDistribution)
        assert obj.sexe is None
        assert obj.tournoi_type is None
        assert obj.tournoi_types3_x3_libelle is None

    def test_to_dict_empty(self):
        from ffbb_api_client_v2.models.terrains_facet_distribution import (
            TerrainsFacetDistribution,
        )

        assert TerrainsFacetDistribution().to_dict() == {}


class TestTournoisFacetDistribution:
    """Cover from_dict with data (True branch) and to_dict."""

    def test_from_dict_with_data(self):
        from ffbb_api_client_v2.models.tournois_facet_distribution import (
            TournoisFacetDistribution,
        )

        data = {
            "sexe": {"Féminin": 5, "Masculin": 10, "Mixte": 3},
            "tournoiType": {"Open Plus": 2, "Open Plus Access": 1, "Open Start": 4},
            "tournoiTypes3x3.libelle": {
                "Open Plus - Junior league 3x3": 1,
                "Open Plus - Super league 3x3": 2,
            },
        }
        obj = TournoisFacetDistribution.from_dict(data)
        assert obj.sexe is not None
        assert obj.sexe.feminine == 5
        assert obj.tournoi_type is not None
        assert obj.tournoi_type.open_plus == 2
        assert obj.tournoi_types3_x3_libelle is not None

    def test_to_dict_with_data(self):
        from ffbb_api_client_v2.models.sexe_class import SexeClass
        from ffbb_api_client_v2.models.tournoi_type_class import TournoiTypeClass
        from ffbb_api_client_v2.models.tournois_facet_distribution import (
            TournoisFacetDistribution,
        )

        obj = TournoisFacetDistribution(
            sexe=SexeClass(feminine=5, masculine=10, mixed=3),
            tournoi_type=TournoiTypeClass(open_plus=2),
        )
        d = obj.to_dict()
        assert "sexe" in d
        assert "tournoiType" in d

    def test_from_dict_empty(self):
        from ffbb_api_client_v2.models.tournois_facet_distribution import (
            TournoisFacetDistribution,
        )

        obj = TournoisFacetDistribution.from_dict({})
        assert obj.to_dict() == {}


# ===========================================================================
# Groupe 3 : Models with uncovered to_dict branches
# ===========================================================================


class TestDocumentFlyer:
    """Cover to_dict branches for fields not exercised in other tests."""

    def test_from_dict_with_extra_fields(self):
        from ffbb_api_client_v2.models.document_flyer import DocumentFlyer

        data = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "storage": "minio",
            "filename_disk": "file.jpg",
            "filename_download": "download.jpg",
            "title": "Test",
            "type": "image/jpeg",
            "uploaded_on": "2024-01-01T00:00:00",
            "modified_on": "2024-06-15T12:00:00",
            "charset": "utf-8",
            "filesize": 1024,
            "width": 800,
            "height": 600,
            "duration": 120,
            "embed": "<iframe></iframe>",
            "description": "A test image",
            "location": "Paris",
            "tags": "test,image",
            "source": "FFBB Serveur",
            "credits": "FFBB",
            "gradient_color": "#ffffff",
            "md5": "abc123",
            "newsbridge_media_id": "nb-123",
            "newsbridge_metadatas": "{}",
            "newsbridge_name": "news",
            "newsbridge_recorded_at": "2024-03-01T10:00:00",
            "focal_point_x": 0.5,
            "focal_point_y": 0.3,
            "newsbridge_labels": ["label1"],
            "newsbridge_persons": ["person1"],
            "uploaded_by": "660e8400-e29b-41d4-a716-446655440000",
            "modified_by": "770e8400-e29b-41d4-a716-446655440000",
            "newsbridge_mission": "mission-1",
        }
        obj = DocumentFlyer.from_dict(data)
        d = obj.to_dict()

        assert d["charset"] == "utf-8"
        assert d["duration"] == 120
        assert d["embed"] == "<iframe></iframe>"
        assert d["description"] == "A test image"
        assert d["location"] == "Paris"
        assert d["tags"] == "test,image"
        assert d["credits"] == "FFBB"
        assert d["newsbridge_media_id"] == "nb-123"
        assert d["newsbridge_metadatas"] == "{}"
        assert d["newsbridge_name"] == "news"
        assert "newsbridge_recorded_at" in d
        assert d["focal_point_x"] == 0.5
        assert d["focal_point_y"] == 0.3
        assert d["uploaded_by"] == "660e8400-e29b-41d4-a716-446655440000"
        assert d["modified_by"] == "770e8400-e29b-41d4-a716-446655440000"
        assert d["newsbridge_mission"] == "mission-1"


class TestExternalCompetitionID:
    def test_from_dict_empty(self):
        from ffbb_api_client_v2.models.external_competition_id import (
            ExternalCompetitionID,
        )

        obj = ExternalCompetitionID.from_dict({})
        assert obj.to_dict() == {}

    def test_roundtrip(self):
        from ffbb_api_client_v2.models.external_competition_id import (
            ExternalCompetitionID,
        )

        data = {
            "code": "C01",
            "nom": "National",
            "sexe": "Masculin",
            "typeCompetition": "Championnat",
        }
        obj = ExternalCompetitionID.from_dict(data)
        d = obj.to_dict()
        assert d == data


class TestTeamEngagement:
    def test_from_dict_empty(self):
        from ffbb_api_client_v2.models.team_engagement import TeamEngagement

        obj = TeamEngagement.from_dict({})
        assert obj.to_dict() == {}

    def test_roundtrip(self):
        from ffbb_api_client_v2.models.team_engagement import TeamEngagement

        data = {
            "nomOfficiel": "Team A",
            "nomUsuel": "TA",
            "codeAbrege": "TA",
        }
        obj = TeamEngagement.from_dict(data)
        d = obj.to_dict()
        assert d["nomOfficiel"] == "Team A"
        assert d["nomUsuel"] == "TA"
        assert d["codeAbrege"] == "TA"


class TestRencontresEngagement:
    def test_to_dict_with_id(self):
        from ffbb_api_client_v2.models.rencontres_engagement import Engagement

        obj = Engagement(id="test")
        assert obj.to_dict() == {"id": "test"}

    def test_from_dict_empty(self):
        from ffbb_api_client_v2.models.rencontres_engagement import Engagement

        obj = Engagement.from_dict({})
        assert obj.to_dict() == {}


class TestSexeClass:
    def test_from_dict_empty(self):
        from ffbb_api_client_v2.models.sexe_class import SexeClass

        obj = SexeClass.from_dict({})
        assert obj.to_dict() == {}

    def test_roundtrip(self):
        from ffbb_api_client_v2.models.sexe_class import SexeClass

        data = {"Féminin": 5, "Masculin": 10, "Mixte": 3}
        obj = SexeClass.from_dict(data)
        assert obj.to_dict() == data


class TestTournoiTypes3X3:
    def test_from_dict_empty(self):
        from ffbb_api_client_v2.models.tournoi_types_3x3 import TournoiTypes3X3

        obj = TournoiTypes3X3.from_dict({})
        assert obj.to_dict() == {}

    def test_roundtrip(self):
        from ffbb_api_client_v2.models.tournoi_types_3x3 import TournoiTypes3X3

        data = {
            "libelle": "Open Plus - Junior league 3x3",
            "logo": "550e8400-e29b-41d4-a716-446655440000",
            "type_league": "junior",
            "type_tournois": 5,
        }
        obj = TournoiTypes3X3.from_dict(data)
        d = obj.to_dict()
        assert d["libelle"] == "Open Plus - Junior league 3x3"
        assert d["logo"] == "550e8400-e29b-41d4-a716-446655440000"
        assert d["type_league"] == "junior"
        assert d["type_tournois"] == "5"


# ===========================================================================
# Groupe 4 : Complex models
# ===========================================================================


class TestOrganismesHit:
    def test_from_dict_invalid_raises_value_error(self):
        from ffbb_api_client_v2.models.organismes_hit import OrganismesHit

        with pytest.raises(ValueError, match="Invalid `OrganismesHit`"):
            OrganismesHit.from_dict("invalid")

    def test_from_dict_empty(self):
        from ffbb_api_client_v2.models.organismes_hit import OrganismesHit

        obj = OrganismesHit.from_dict({})
        assert isinstance(obj, OrganismesHit)
        assert obj.to_dict() == {}


class TestLive:
    """Cover to_dict branches for OT scores, external_id, team_engagements."""

    def test_to_dict_ot_scores_and_nested(self):
        from ffbb_api_client_v2.models.external_id import ExternalID
        from ffbb_api_client_v2.models.live import Live
        from ffbb_api_client_v2.models.team_engagement import TeamEngagement

        obj = Live(
            score_ot1_home=10,
            score_ot2_home=5,
            score_ot1_out=8,
            score_ot2_out=3,
            external_id=ExternalID(nom_equipe1="Team A", nom_equipe2="Team B"),
            team_engagement_home=TeamEngagement(nom_officiel="Home Team"),
            team_engagement_out=TeamEngagement(nom_officiel="Away Team"),
        )
        d = obj.to_dict()
        assert d["score_ot1_home"] == 10
        assert d["score_ot2_home"] == 5
        assert d["score_ot1_out"] == 8
        assert d["score_ot2_out"] == 3
        assert d["externalId"]["nomEquipe1"] == "Team A"
        assert d["teamEngagement_home"]["nomOfficiel"] == "Home Team"
        assert d["teamEngagement_out"]["nomOfficiel"] == "Away Team"


# ===========================================================================
# Groupe 5 : converter_utils edge cases
# ===========================================================================


class TestFromOfficielsListEdgeCases:
    """Cover all branches of from_officiels_list."""

    def test_non_empty_string(self):
        from ffbb_api_client_v2.utils.converter_utils import from_officiels_list

        result = from_officiels_list("Alice, Bob, Charlie")
        assert result == ["Alice", "Bob", "Charlie"]

    def test_empty_string(self):
        from ffbb_api_client_v2.utils.converter_utils import from_officiels_list

        result = from_officiels_list("")
        assert result is None

    def test_list_passthrough(self):
        from ffbb_api_client_v2.utils.converter_utils import from_officiels_list

        data = [{"name": "Alice"}, {"name": "Bob"}]
        result = from_officiels_list(data)
        assert result is data

    def test_none_returns_none(self):
        from ffbb_api_client_v2.utils.converter_utils import from_officiels_list

        assert from_officiels_list(None) is None

    def test_invalid_type_returns_none(self):
        from ffbb_api_client_v2.utils.converter_utils import from_officiels_list

        assert from_officiels_list(42) is None


class TestFromStrExceptionPath:
    """Cover the TypeError/ValueError exception path in from_str (lines 102-109)."""

    def test_object_whose_str_raises_type_error(self, caplog):
        from ffbb_api_client_v2.utils.converter_utils import from_str

        class BadStr:
            def __str__(self):
                raise TypeError("cannot convert")

        with caplog.at_level(
            logging.WARNING, logger="ffbb_api_client_v2.utils.converter_utils"
        ):
            result = from_str({"k": BadStr()}, "k")
        assert result is None
        assert "cannot convert" in caplog.text


# ===========================================================================
# Groupe 6 : Additional coverage for modules still < 90%
# ===========================================================================


class TestPratiquesFacetStats:
    def test_from_dict_and_to_dict(self):
        from ffbb_api_client_v2.models.pratiques_facet_stats import PratiquesFacetStats

        obj = PratiquesFacetStats.from_dict({})
        assert isinstance(obj, PratiquesFacetStats)
        assert obj.to_dict() == {}


class TestCompetitionsFacetDistributionWithData:
    """Cover to_dict branches when nested objects are populated."""

    def test_to_dict_with_nested_objects(self):
        from ffbb_api_client_v2.models.competition_id_sexe import CompetitionIDSexe
        from ffbb_api_client_v2.models.competition_id_type_competition import (
            CompetitionIDTypeCompetition,
        )
        from ffbb_api_client_v2.models.competitions_facet_distribution import (
            CompetitionsFacetDistribution,
        )
        from ffbb_api_client_v2.models.niveau_class import NiveauClass

        obj = CompetitionsFacetDistribution(
            competition_id_categorie_code={"U13": 5},
            competition_id_nom_extended={"National": 3},
            competition_id_sexe=CompetitionIDSexe(feminine=2, masculine=8),
            competition_id_type_competition=CompetitionIDTypeCompetition(
                championnat=10
            ),
            niveau=NiveauClass(départemental=4),
            organisateur_id={"org1": 1},
            organisateur_nom={"FFBB": 2},
        )
        d = obj.to_dict()
        assert d["competitionId.categorie.code"] == {"U13": 5}
        assert d["competitionId.nomExtended"] == {"National": 3}
        assert "competitionId.sexe" in d
        assert "competitionId.typeCompetition" in d
        assert "niveau" in d
        assert d["organisateur.id"] == {"org1": 1}
        assert d["organisateur.nom"] == {"FFBB": 2}


class TestRencontresFacetDistributionWithData:
    """Cover to_dict branches when nested objects are populated."""

    def test_to_dict_with_nested_objects(self):
        from ffbb_api_client_v2.models.competition_id_sexe import CompetitionIDSexe
        from ffbb_api_client_v2.models.competition_id_type_competition import (
            CompetitionIDTypeCompetition,
        )
        from ffbb_api_client_v2.models.niveau_class import NiveauClass
        from ffbb_api_client_v2.models.rencontres_facet_distribution import (
            RencontresFacetDistribution,
        )

        obj = RencontresFacetDistribution(
            competition_id_categorie_code={"U13": 5},
            competition_id_nom_extended={"National": 3},
            competition_id_sexe=CompetitionIDSexe(feminine=2, masculine=8),
            competition_id_type_competition=CompetitionIDTypeCompetition(
                championnat=10
            ),
            niveau=NiveauClass(départemental=4),
            organisateur_id={"org1": 1},
            organisateur_nom={"FFBB": 2},
        )
        d = obj.to_dict()
        assert d["competitionId.categorie.code"] == {"U13": 5}
        assert d["competitionId.nomExtended"] == {"National": 3}
        assert "competitionId.sexe" in d
        assert "competitionId.typeCompetition" in d
        assert "niveau" in d
        assert d["organisateur.id"] == {"org1": 1}
        assert d["organisateur.nom"] == {"FFBB": 2}
