"""Tests for v2 backport features: engagements, formations, filter/sort/limit, ABC QueryFieldsManager."""

from __future__ import annotations

import unittest
from abc import ABC

from ffbb_api_client_v3.config import (
    MEILISEARCH_FACETS_ENGAGEMENTS,
    MEILISEARCH_FACETS_FORMATIONS,
    MEILISEARCH_INDEX_ENGAGEMENTS,
    MEILISEARCH_INDEX_FORMATIONS,
)
from ffbb_api_client_v3.models.engagements_facet_distribution import (
    EngagementsFacetDistribution,
)
from ffbb_api_client_v3.models.engagements_facet_stats import EngagementsFacetStats
from ffbb_api_client_v3.models.engagements_hit import EngagementsHit
from ffbb_api_client_v3.models.engagements_multi_search_query import (
    EngagementsMultiSearchQuery,
)
from ffbb_api_client_v3.models.field_set import FieldSet
from ffbb_api_client_v3.models.formation_session import FormationSession
from ffbb_api_client_v3.models.formations_facet_distribution import (
    FormationsFacetDistribution,
)
from ffbb_api_client_v3.models.formations_facet_stats import FormationsFacetStats
from ffbb_api_client_v3.models.formations_hit import FormationsHit
from ffbb_api_client_v3.models.formations_multi_search_query import (
    FormationsMultiSearchQuery,
)
from ffbb_api_client_v3.models.multi_search_result_engagements import (
    EngagementsMultiSearchResult,
)
from ffbb_api_client_v3.models.multi_search_result_formations import (
    FormationsMultiSearchResult,
)
from ffbb_api_client_v3.models.organismes_multi_search_query import (
    OrganismesMultiSearchQuery,
)
from ffbb_api_client_v3.models.query_fields_manager import QueryFieldsManager


class TestEngagementsHit(unittest.TestCase):
    """Test EngagementsHit model."""

    def test_from_dict_minimal(self) -> None:
        data = {"id": "123", "nom": "Clermont Basket"}
        hit = EngagementsHit.from_dict(data)
        assert hit.id == "123"
        assert hit.nom == "Clermont Basket"
        assert hit.lower_nom == "clermont basket"

    def test_from_dict_full(self) -> None:
        data = {
            "id": "456",
            "nom": "Equipe 1",
            "age": "SEN",
            "sexe": "Masculin",
            "clubPro": False,
            "codeAbrege": "CLR",
            "codeClub": "0063001",
            "nomClub": "Clermont Basket",
            "nomEquipe": "Clermont 1",
            "nomOrganisme": "Clermont Basketball",
            "numeroEquipe": "1",
            "_geo": {"lat": 45.7, "lng": 3.08},
        }
        hit = EngagementsHit.from_dict(data)
        assert hit.sexe == "Masculin"
        assert hit.club_pro is False
        assert hit.code_abrege == "CLR"
        assert hit.geo is not None
        assert hit.geo.lat == 45.7

    def test_to_dict_round_trip(self) -> None:
        data = {"id": "789", "nom": "Test", "nomClub": "Club A", "clubPro": True}
        hit1 = EngagementsHit.from_dict(data)
        d1 = hit1.to_dict()
        hit2 = EngagementsHit.from_dict(d1)
        d2 = hit2.to_dict()
        assert d1 == d2

    def test_is_valid_for_query(self) -> None:
        hit = EngagementsHit.from_dict({"id": "1", "nom": "ABC Lyon"})
        assert hit.is_valid_for_query("lyon")
        assert hit.is_valid_for_query("")
        assert not hit.is_valid_for_query("paris")

    def test_from_dict_type_error(self) -> None:
        with self.assertRaises(TypeError):
            EngagementsHit.from_dict("not a dict")


class TestFormationsHit(unittest.TestCase):
    """Test FormationsHit model."""

    def test_from_dict_minimal(self) -> None:
        data = {"id": "abc-123", "title": "Formation Coach"}
        hit = FormationsHit.from_dict(data)
        assert hit.id == "abc-123"
        assert hit.title == "Formation Coach"
        assert hit.lower_title == "formation coach"

    def test_from_dict_with_session(self) -> None:
        data = {
            "id": "f-1",
            "title": "Formation Arbitre",
            "domain": "Arbitrage",
            "mode": "presentiel",
            "sessions": [
                {"id": "s-1", "title": "Session 1", "place": "Paris"},
            ],
        }
        hit = FormationsHit.from_dict(data)
        assert hit.sessions is not None
        assert len(hit.sessions) == 1
        assert hit.sessions[0].place == "Paris"

    def test_to_dict_round_trip(self) -> None:
        data = {"id": "f-2", "title": "Test", "domain": "D", "theme": "T"}
        hit1 = FormationsHit.from_dict(data)
        d1 = hit1.to_dict()
        hit2 = FormationsHit.from_dict(d1)
        d2 = hit2.to_dict()
        assert d1 == d2

    def test_is_valid_for_query(self) -> None:
        hit = FormationsHit.from_dict(
            {"id": "1", "title": "Coach Niveau 1", "domain": "Coaching"}
        )
        assert hit.is_valid_for_query("coach")
        assert hit.is_valid_for_query("coaching")
        assert not hit.is_valid_for_query("arbitre")

    def test_from_dict_type_error(self) -> None:
        with self.assertRaises(TypeError):
            FormationsHit.from_dict("not a dict")


class TestFormationSession(unittest.TestCase):
    """Test FormationSession model."""

    def test_from_dict(self) -> None:
        data = {
            "id": "s-1",
            "title": "Session A",
            "place": "Lyon",
            "postal_code": "69000",
        }
        session = FormationSession.from_dict(data)
        assert session.id == "s-1"
        assert session.place == "Lyon"

    def test_to_dict_round_trip(self) -> None:
        data = {"id": "s-2", "title": "Session B", "entity": "FFBB"}
        s1 = FormationSession.from_dict(data)
        d1 = s1.to_dict()
        s2 = FormationSession.from_dict(d1)
        d2 = s2.to_dict()
        assert d1 == d2


class TestEngagementsFacets(unittest.TestCase):
    """Test Engagements facet distribution and stats."""

    def test_facet_distribution_from_dict(self) -> None:
        data = {
            "clubPro": {"true": 10, "false": 500},
            "idCompetition.sexe": {"Masculin": 200, "Féminin": 180},
            "niveau.code": {"SEN": 50, "U17": 30},
        }
        fd = EngagementsFacetDistribution.from_dict(data)
        assert fd.club_pro == {"true": 10, "false": 500}
        assert fd.id_competition_sexe == {"Masculin": 200, "Féminin": 180}
        assert fd.niveau_code == {"SEN": 50, "U17": 30}

    def test_facet_distribution_to_dict(self) -> None:
        data = {"niveau.code": {"SEN": 5}}
        fd1 = EngagementsFacetDistribution.from_dict(data)
        d1 = fd1.to_dict()
        fd2 = EngagementsFacetDistribution.from_dict(d1)
        d2 = fd2.to_dict()
        assert d1 == d2

    def test_facet_stats(self) -> None:
        stats = EngagementsFacetStats.from_dict({})
        assert stats.to_dict() == {}


class TestFormationsFacets(unittest.TestCase):
    """Test Formations facet distribution and stats."""

    def test_facet_distribution_from_dict(self) -> None:
        data = {
            "domain": {"Coaching": 10},
            "mode": {"presentiel": 40, "distanciel": 20},
        }
        fd = FormationsFacetDistribution.from_dict(data)
        assert fd.domain == {"Coaching": 10}
        assert fd.mode == {"presentiel": 40, "distanciel": 20}

    def test_facet_stats(self) -> None:
        stats = FormationsFacetStats.from_dict({})
        assert stats.to_dict() == {}


class TestEngagementsMultiSearchQuery(unittest.TestCase):
    """Test EngagementsMultiSearchQuery construction."""

    def test_default_query(self) -> None:
        q = EngagementsMultiSearchQuery("Clermont")
        d = q.to_dict()
        assert d["indexUid"] == MEILISEARCH_INDEX_ENGAGEMENTS
        assert d["q"] == "Clermont"
        assert d["facets"] == MEILISEARCH_FACETS_ENGAGEMENTS
        assert d["limit"] == 10

    def test_query_with_filter_sort(self) -> None:
        q = EngagementsMultiSearchQuery(
            "Lyon",
            limit=5,
            filter=['niveau.code = "SEN"'],
            sort=["nom:asc"],
        )
        d = q.to_dict()
        assert d["limit"] == 5
        assert d["filter"] == ['niveau.code = "SEN"']
        assert d["sort"] == ["nom:asc"]


class TestFormationsMultiSearchQuery(unittest.TestCase):
    """Test FormationsMultiSearchQuery construction."""

    def test_default_query(self) -> None:
        q = FormationsMultiSearchQuery("arbitre")
        d = q.to_dict()
        assert d["indexUid"] == MEILISEARCH_INDEX_FORMATIONS
        assert d["q"] == "arbitre"
        assert d["facets"] == MEILISEARCH_FACETS_FORMATIONS

    def test_query_with_filter(self) -> None:
        q = FormationsMultiSearchQuery(
            "",
            filter=['mode = "presentiel"'],
            limit=50,
        )
        d = q.to_dict()
        assert d["filter"] == ['mode = "presentiel"']
        assert d["limit"] == 50


class TestOrganismesQueryFilterSortLimit(unittest.TestCase):
    """Test that existing query classes correctly pass filter/sort/limit."""

    def test_organismes_with_filter_sort(self) -> None:
        q = OrganismesMultiSearchQuery(
            "Paris",
            limit=5,
            filter=['type = "ASS"'],
            sort=["nom:asc"],
        )
        d = q.to_dict()
        assert d["q"] == "Paris"
        assert d["limit"] == 5
        assert d["filter"] == ['type = "ASS"']
        assert d["sort"] == ["nom:asc"]


class TestFieldSetValues(unittest.TestCase):
    """Test that FieldSet members have distinct values."""

    def test_basic_distinct_from_default(self) -> None:
        assert FieldSet.BASIC != FieldSet.DEFAULT

    def test_detailed_distinct_from_default(self) -> None:
        assert FieldSet.DETAILED != FieldSet.DEFAULT

    def test_minimal_distinct(self) -> None:
        assert FieldSet.MINIMAL != FieldSet.DEFAULT


class TestQueryFieldsManagerABC(unittest.TestCase):
    """Test that QueryFieldsManager is now an ABC."""

    def test_is_abstract(self) -> None:
        assert issubclass(QueryFieldsManager, ABC)

    def test_cannot_instantiate_directly(self) -> None:
        with self.assertRaises(TypeError):
            QueryFieldsManager()  # type: ignore[abstract]

    def test_static_methods_still_work(self) -> None:
        fields = QueryFieldsManager.get_organisme_fields()
        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_subclass_works(self) -> None:
        class MyFields(QueryFieldsManager):
            def get_fields(self) -> list[str]:
                return ["id", "nom"]

        instance = MyFields()
        assert instance.get_fields() == ["id", "nom"]
        # Static methods still accessible from subclass
        assert len(instance.get_competition_fields()) > 0


class TestMultiSearchResultEngagements(unittest.TestCase):
    """Test EngagementsMultiSearchResult deserialization."""

    def test_from_dict(self) -> None:
        data = {
            "indexUid": "ffbbserver_engagements",
            "hits": [{"id": "1", "nom": "Test"}],
            "query": "test",
            "processingTimeMs": 5,
            "limit": 10,
            "offset": 0,
            "estimatedTotalHits": 1,
            "facetDistribution": {"clubPro": {"true": 1}},
            "facetStats": {},
        }
        result = EngagementsMultiSearchResult.from_dict(data)
        assert result.index_uid == "ffbbserver_engagements"
        assert result.hits is not None
        assert len(result.hits) == 1
        assert result.hits[0].nom == "Test"
        assert isinstance(result.facet_distribution, EngagementsFacetDistribution)


class TestMultiSearchResultFormations(unittest.TestCase):
    """Test FormationsMultiSearchResult deserialization."""

    def test_from_dict(self) -> None:
        data = {
            "indexUid": "ffbbserver_formations",
            "hits": [{"id": "f-1", "title": "Coach Niveau 1"}],
            "query": "coach",
            "processingTimeMs": 3,
            "limit": 10,
            "offset": 0,
            "estimatedTotalHits": 1,
            "facetDistribution": {"domain": {"Coaching": 1}},
            "facetStats": {},
        }
        result = FormationsMultiSearchResult.from_dict(data)
        assert result.index_uid == "ffbbserver_formations"
        assert result.hits is not None
        assert len(result.hits) == 1
        assert result.hits[0].title == "Coach Niveau 1"
        assert isinstance(result.facet_distribution, FormationsFacetDistribution)


class TestConfigIndexes(unittest.TestCase):
    """Test that new index constants exist in config."""

    def test_engagements_index(self) -> None:
        assert MEILISEARCH_INDEX_ENGAGEMENTS == "ffbbserver_engagements"

    def test_formations_index(self) -> None:
        assert MEILISEARCH_INDEX_FORMATIONS == "ffbbserver_formations"

    def test_facets_defined(self) -> None:
        assert isinstance(MEILISEARCH_FACETS_ENGAGEMENTS, list)
        assert isinstance(MEILISEARCH_FACETS_FORMATIONS, list)
        assert "niveau.code" in MEILISEARCH_FACETS_ENGAGEMENTS
        assert "domain" in MEILISEARCH_FACETS_FORMATIONS


if __name__ == "__main__":
    unittest.main()
