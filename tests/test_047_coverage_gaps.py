"""Tests to bring all modules to ≥90% coverage.

Targets files identified as <90% after the converter refactoring:
- Models: to_dict branches for non-None fields
- Utils: cache_manager, retry_utils, secure_logging edge cases
- multi_search_queries, multi_search_query, multi_search_results
"""

from __future__ import annotations

import logging
from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import UUID

import pytest

# ---------------------------------------------------------------------------
# Model to_dict coverage
# ---------------------------------------------------------------------------


class TestCategorieToDictCoverage:
    """categorie.py — cover to_dict branches for all fields."""

    def test_to_dict_all_fields(self):
        from ffbb_api_client_v2.models.categorie import Categorie

        now = datetime(2024, 6, 15, 12, 0, 0)
        c = Categorie(
            code="U13",
            date_created=now,
            date_updated=now,
            categorie_id="cat-1",
            libelle="Under 13",
            ordre=3,
        )
        d = c.to_dict()
        assert d["code"] == "U13"
        assert d["date_created"] == now.isoformat()
        assert d["date_updated"] == now.isoformat()
        assert d["id"] == "cat-1"
        assert d["libelle"] == "Under 13"
        assert d["ordre"] == 3


class TestCartographieToDictCoverage:
    """cartographie.py — cover to_dict branches."""

    def test_to_dict_all_fields(self):
        from ffbb_api_client_v2.models.cartographie import Cartographie
        from ffbb_api_client_v2.models.coordonnees import Coordonnees

        coords = Coordonnees(coordinates=[2.35, 48.85], type="Point")
        c = Cartographie(
            adresse="1 rue du Panier",
            code_postal=75001,
            coordonnees=coords,
            date_created=None,
            date_updated=None,
            cartographie_id="carto-1",
            latitude=48.85,
            longitude=2.35,
            title="Salle A",
            ville="Paris",
            status="published",
        )
        d = c.to_dict()
        assert d["adresse"] == "1 rue du Panier"
        assert d["codePostal"] == "75001"
        assert d["coordonnees"] == coords.to_dict()
        assert d["id"] == "carto-1"
        assert d["latitude"] == 48.85
        assert d["longitude"] == 2.35
        assert d["title"] == "Salle A"
        assert d["ville"] == "Paris"
        assert d["status"] == "published"


class TestFolderToDictCoverage:
    """folder.py — cover to_dict branches for id and name."""

    def test_to_dict_all_fields(self):
        from ffbb_api_client_v2.models.folder import Folder

        uid = UUID("12345678-1234-1234-1234-123456789abc")
        f = Folder(id=uid, name="images", parent=None)
        d = f.to_dict()
        assert d["id"] == str(uid)
        assert d["name"] == "images"
        assert "parent" not in d  # parent is None


class TestIDPouleToDictCoverage:
    """id_poule.py — cover to_dict nom branch."""

    def test_to_dict_with_nom(self):
        from ffbb_api_client_v2.models.id_poule import IDPoule

        p = IDPoule(id="poule-1", nom="Poule A")
        d = p.to_dict()
        assert d["id"] == "poule-1"
        assert d["nom"] == "Poule A"


class TestPouleToDictCoverage:
    """poule.py — cover to_dict engagements branch."""

    def test_to_dict_with_engagements(self):
        from ffbb_api_client_v2.models.poule import Poule
        from ffbb_api_client_v2.models.rencontres_engagement import Engagement

        eng = Engagement.from_dict({"nomEquipe": "Team A"})
        p = Poule(nom="Poule A", id="p-1", engagements=[eng])
        d = p.to_dict()
        assert d["nom"] == "Poule A"
        assert d["id"] == "p-1"
        assert isinstance(d["engagements"], list)
        assert len(d["engagements"]) == 1


class TestSaisonToDictCoverage:
    """saison.py — cover to_dict code branch."""

    def test_to_dict_with_code(self):
        from ffbb_api_client_v2.models.saison import Saison

        s = Saison(code="2024")
        d = s.to_dict()
        assert d["code"] == "2024"


class TestTypeClassToDictCoverage:
    """type_class.py — cover to_dict groupement branch."""

    def test_to_dict_with_groupement(self):
        from ffbb_api_client_v2.models.type_class import TypeClass

        t = TypeClass(groupement=5)
        d = t.to_dict()
        assert d["Groupement"] == 5


class TestExternalIDToDictCoverage:
    """external_id.py — cover to_dict branches for CompetitionID and ExternalID."""

    def test_competition_id_to_dict(self):
        from ffbb_api_client_v2.models.external_id import ExternalCompetitionID

        c = ExternalCompetitionID(
            code="NM1",
            nom="Nationale 1",
            sexe="Masculin",
            type_competition="Championnat",
        )
        d = c.to_dict()
        assert d["code"] == "NM1"
        assert d["nom"] == "Nationale 1"
        assert d["sexe"] == "Masculin"
        assert d["typeCompetition"] == "Championnat"

    def test_external_id_to_dict_all_fields(self):
        from ffbb_api_client_v2.models.external_id import (
            ExternalCompetitionID,
            ExternalID,
        )
        from ffbb_api_client_v2.models.id_organisme_equipe import IDOrganismeEquipe
        from ffbb_api_client_v2.models.id_poule import IDPoule
        from ffbb_api_client_v2.models.salle import Salle

        comp = ExternalCompetitionID(
            code="NM1", nom="Nationale 1", sexe="M", type_competition="Champ"
        )
        org1 = IDOrganismeEquipe(
            id="o1",
            nom="Club A",
            nom_simple=None,
            code="CA",
            nom_club_pro=None,
            logo=None,
        )
        org2 = IDOrganismeEquipe(
            id="o2",
            nom="Club B",
            nom_simple=None,
            code="CB",
            nom_club_pro=None,
            logo=None,
        )
        salle = Salle.from_dict({"libelle": "Salle X", "adresse": "1 rue"})
        poule = IDPoule(id="p1", nom="Poule A")
        ext = ExternalID(
            nom_equipe1="Eq1",
            nom_equipe2="Eq2",
            numero_journee=5,
            competition_id=comp,
            id_organisme_equipe1=org1,
            id_organisme_equipe2=org2,
            salle=salle,
            id_poule=poule,
        )
        d = ext.to_dict()
        assert d["nomEquipe1"] == "Eq1"
        assert d["nomEquipe2"] == "Eq2"
        assert d["numeroJournee"] == "5"
        assert d["competitionId"]["code"] == "NM1"
        assert "idOrganismeEquipe1" in d
        assert "idOrganismeEquipe2" in d
        assert d["salle"]["libelle"] == "Salle X"
        assert d["idPoule"]["id"] == "p1"


class TestDocumentFlyerToDictCoverage:
    """document_flyer.py — cover to_dict branches."""

    def test_to_dict_populated_fields(self):
        from ffbb_api_client_v2.models.document_flyer import DocumentFlyer
        from ffbb_api_client_v2.models.document_flyer_type import DocumentFlyerType
        from ffbb_api_client_v2.models.folder import Folder
        from ffbb_api_client_v2.models.source import Source

        uid = UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
        now = datetime(2024, 1, 15, 10, 30, 0)
        folder = Folder(id=uid, name="docs", parent=None)
        doc = DocumentFlyer(
            id=uid,
            storage="local",
            filename_disk="file.pdf",
            filename_download="file.pdf",
            title="Flyer",
            type=DocumentFlyerType.IMAGE_JPEG,
            uploaded_on=now,
            modified_on=now,
            filesize=1024,
            width=800,
            height=600,
            source=Source.FFBB_SERVEUR,
            gradient_color="#fff",
            md5="abc123def456",
            newsbridge_labels=["label1"],
            newsbridge_persons=["person1"],
            folder=folder,
        )
        d = doc.to_dict()
        assert d["id"] == str(uid)
        assert d["storage"] == "local"
        assert d["filename_disk"] == "file.pdf"
        assert d["filename_download"] == "file.pdf"
        assert d["title"] == "Flyer"
        assert d["type"] == DocumentFlyerType.IMAGE_JPEG.value
        assert d["uploaded_on"] == now.isoformat()
        assert d["modified_on"] == now.isoformat()
        assert d["filesize"] == "1024"
        assert d["width"] == 800
        assert d["height"] == 600
        assert d["source"] == Source.FFBB_SERVEUR.value
        assert d["gradient_color"] == "#fff"
        assert "md5" in d
        assert d["newsbridge_labels"] == ["label1"]
        assert "newsbridge_persons" in d
        assert d["folder"]["name"] == "docs"


class TestTournoisToDictCoverage:
    """multi_search_result_tournois.py — cover SexeClass and TournoisFacetDistribution to_dict."""

    def test_sexe_class_to_dict(self):
        from ffbb_api_client_v2.models.sexe_class import SexeClass

        s = SexeClass(feminine=3, masculine=5, mixed=2)
        d = s.to_dict()
        assert d["Féminin"] == 3
        assert d["Masculin"] == 5
        assert d["Mixte"] == 2

    def test_tournois_facet_distribution_to_dict(self):
        from ffbb_api_client_v2.models.sexe_class import SexeClass
        from ffbb_api_client_v2.models.tournoi_type_class import TournoiTypeClass
        from ffbb_api_client_v2.models.tournois_facet_distribution import (
            TournoisFacetDistribution,
        )

        sexe = SexeClass(feminine=1, masculine=2, mixed=0)
        tt = TournoiTypeClass.from_dict({"Terrain": 3})
        fd = TournoisFacetDistribution(
            sexe=sexe, tournoi_type=tt, tournoi_types3_x3_libelle=None
        )
        d = fd.to_dict()
        assert d["sexe"]["Féminin"] == 1
        assert "tournoiType" in d

    def test_tournois_hit_to_dict(self):
        from ffbb_api_client_v2.models.cartographie import Cartographie
        from ffbb_api_client_v2.models.commune import Commune
        from ffbb_api_client_v2.models.geo import Geo
        from ffbb_api_client_v2.models.nature_sol import NatureSol
        from ffbb_api_client_v2.models.tournois_hit import TournoisHit
        from ffbb_api_client_v2.models.tournois_hit_type import HitType

        now = datetime(2024, 6, 1, 12, 0, 0)
        commune = Commune.from_dict({"libelle": "Paris", "departement": "75"})
        geo = Geo.from_dict({"lat": 48.85, "lng": 2.35})
        hit = TournoisHit(
            nom="Terrain A",
            rue="1 rue du Sport",
            id=42,
            acces_libre=True,
            date_created=now,
            date_updated=now,
            largeur=20,
            longueur=40,
            numero=1,
            cartographie=Cartographie(
                adresse="addr",
                code_postal=75001,
                coordonnees=None,
                date_created=None,
                date_updated=None,
                cartographie_id="c1",
                latitude=48.85,
                longitude=2.35,
                title="T",
                ville="Paris",
                status="published",
            ),
            commune=commune,
            nature_sol=NatureSol.from_dict({"libelle": "Béton"}),
            geo=geo,
            thumbnail=None,
            type=HitType.TERRAIN,
        )
        d = hit.to_dict()
        assert d["nom"] == "Terrain A"
        assert d["rue"] == "1 rue du Sport"
        assert "id" in d
        assert d["accesLibre"] is True
        assert "date_created" in d
        assert "date_updated" in d
        assert d["largeur"] == 20
        assert d["longueur"] == 40
        assert d["numero"] == 1
        assert "cartographie" in d
        assert "commune" in d
        assert "natureSol" in d
        assert "_geo" in d
        assert d["type"] == "Terrain"


# ---------------------------------------------------------------------------
# MultiSearchQueries coverage (50% → 90%+)
# ---------------------------------------------------------------------------


class TestMultiSearchQueriesCoverage:
    """multi_search_queries.py — cover from_dict and to_dict."""

    def test_from_dict_with_queries(self):
        from ffbb_api_client_v2.models.multi_search_queries import MultiSearchQueries

        data = {
            "queries": [
                {
                    "indexUid": "ffbbserver_organismes",
                    "q": "test",
                    "limit": 10,
                    "offset": 0,
                }
            ]
        }
        result = MultiSearchQueries.from_dict(data)
        assert result.queries is not None
        assert len(result.queries) == 1

    def test_from_dict_none_queries(self):
        from ffbb_api_client_v2.models.multi_search_queries import MultiSearchQueries

        result = MultiSearchQueries.from_dict({"queries": None})
        assert result.queries is None

    def test_to_dict_with_queries(self):
        from ffbb_api_client_v2.models.multi_search_queries import MultiSearchQueries
        from ffbb_api_client_v2.models.multi_search_query import MultiSearchQuery

        q = MultiSearchQuery(index_uid="ffbbserver_organismes", q="test")
        msq = MultiSearchQueries(queries=[q])
        d = msq.to_dict()
        assert "queries" in d
        assert len(d["queries"]) == 1

    def test_to_dict_empty(self):
        from ffbb_api_client_v2.models.multi_search_queries import MultiSearchQueries

        msq = MultiSearchQueries(queries=None)
        d = msq.to_dict()
        assert d == {}


# ---------------------------------------------------------------------------
# MultiSearchQuery coverage (85% → 90%+)
# ---------------------------------------------------------------------------


class TestMultiSearchQueryCoverage:
    """multi_search_query.py — cover from_dict, to_dict, is_valid_result, filter_result."""

    def test_from_dict(self):
        from ffbb_api_client_v2.models.multi_search_query import MultiSearchQuery

        data = {
            "indexUid": "ffbbserver_organismes",
            "q": "paris",
            "facets": ["type"],
            "limit": 20,
            "offset": 5,
            "filter": ["type = Club"],
            "sort": ["nom:asc"],
        }
        q = MultiSearchQuery.from_dict(data)
        assert q.index_uid == "ffbbserver_organismes"
        assert q.q == "paris"
        assert q.facets == ["type"]
        assert q.limit == 20
        assert q.offset == 5
        assert q.filter == ["type = Club"]
        assert q.sort == ["nom:asc"]

    def test_to_dict_all_fields(self):
        from ffbb_api_client_v2.models.multi_search_query import MultiSearchQuery

        q = MultiSearchQuery(
            index_uid="ffbbserver_organismes",
            q="paris",
            facets=["type"],
            limit=20,
            offset=5,
            filter=["type = Club"],
            sort=["nom:asc"],
        )
        d = q.to_dict()
        assert d["indexUid"] == "ffbbserver_organismes"
        assert d["q"] == "paris"
        assert d["facets"] == ["type"]
        assert d["limit"] == 20
        assert d["offset"] == 5
        assert d["filter"] == ["type = Club"]
        assert d["sort"] == ["nom:asc"]

    def test_is_valid_hit(self):
        from ffbb_api_client_v2.models.multi_search_query import MultiSearchQuery

        q = MultiSearchQuery(index_uid="test", q="test")
        assert q.is_valid_hit(MagicMock()) is True

    def test_filter_result_removes_invalid_hits(self):
        from ffbb_api_client_v2.models.multi_search_query import MultiSearchQuery

        q = MultiSearchQuery(index_uid="test", q="paris")

        # Create mock hits
        valid_hit = MagicMock()
        valid_hit.is_valid_for_query.return_value = True
        invalid_hit = MagicMock()
        invalid_hit.is_valid_for_query.return_value = False

        result = MagicMock()
        result.hits = [valid_hit, invalid_hit]
        result.estimated_total_hits = 2

        filtered = q.filter_result(result)
        assert filtered.estimated_total_hits == 1
        assert invalid_hit not in filtered.hits

    def test_filter_result_no_query(self):
        from ffbb_api_client_v2.models.multi_search_query import MultiSearchQuery

        q = MultiSearchQuery(index_uid="test", q=None)
        result = MagicMock()
        result.hits = [MagicMock()]
        filtered = q.filter_result(result)
        assert filtered is result  # Unchanged


# ---------------------------------------------------------------------------
# MultiSearchResults to_dict coverage (89% → 90%+)
# ---------------------------------------------------------------------------


class TestMultiSearchResultsToDictCoverage:
    """multi_search_results.py — cover to_dict branches."""

    def test_multi_search_result_to_dict_all_fields(self):
        from ffbb_api_client_v2.models.multi_search_result_organismes import (
            OrganismesMultiSearchResult,
        )
        from ffbb_api_client_v2.models.organismes_facet_distribution import (
            OrganismesFacetDistribution,
        )
        from ffbb_api_client_v2.models.organismes_facet_stats import (
            OrganismesFacetStats,
        )
        from ffbb_api_client_v2.models.organismes_hit import OrganismesHit

        hit = OrganismesHit.from_dict({"nom": "Club A", "code": "CL01"})
        fd = OrganismesFacetDistribution.from_dict({})
        fs = OrganismesFacetStats.from_dict({})
        result = OrganismesMultiSearchResult(
            index_uid="ffbbserver_organismes",
            hits=[hit],
            query="test",
            processing_time_ms=5,
            limit=10,
            offset=0,
            estimated_total_hits=1,
            facet_distribution=fd,
            facet_stats=fs,
        )
        d = result.to_dict()
        assert d["indexUid"] == "ffbbserver_organismes"
        assert len(d["hits"]) == 1
        assert d["query"] == "test"
        assert d["processingTimeMs"] == 5
        assert d["limit"] == 10
        assert d["offset"] == 0
        assert d["estimatedTotalHits"] == 1
        assert "facetDistribution" in d
        assert "facetStats" in d


# ---------------------------------------------------------------------------
# FacetDistribution / FacetStats (89% — assert False branch)
# ---------------------------------------------------------------------------


class TestFacetDistributionAssertFalse:
    """facet_distribution.py / facet_stats.py — cover the assert False line."""

    def test_facet_distribution_from_dict_non_dict_fails(self):
        from ffbb_api_client_v2.models.facet_distribution import FacetDistribution

        with pytest.raises(AssertionError):
            FacetDistribution.from_dict("not a dict")

    def test_facet_stats_from_dict_non_dict_fails(self):
        from ffbb_api_client_v2.models.facet_stats import FacetStats

        with pytest.raises(AssertionError):
            FacetStats.from_dict("not a dict")


# ---------------------------------------------------------------------------
# SecureLogging coverage (85% → 90%+)
# ---------------------------------------------------------------------------


class TestSecureLoggingCoverage:
    """secure_logging.py — cover error, critical, log, and non-string message."""

    def test_mask_non_string_message(self):
        from ffbb_api_client_v2.utils.secure_logging import SecureLogger

        sl = SecureLogger("test_mask", level=logging.DEBUG)
        result = sl._mask_sensitive_data(12345)
        assert result == "12345"

    def test_error_level(self, caplog):
        from ffbb_api_client_v2.utils.secure_logging import SecureLogger

        sl = SecureLogger("test_error", level=logging.DEBUG)
        with caplog.at_level(logging.ERROR, logger="test_error"):
            sl.error("Something failed")
        assert "Something failed" in caplog.text

    def test_critical_level(self, caplog):
        from ffbb_api_client_v2.utils.secure_logging import SecureLogger

        sl = SecureLogger("test_critical", level=logging.DEBUG)
        with caplog.at_level(logging.CRITICAL, logger="test_critical"):
            sl.critical("Critical failure")
        assert "Critical failure" in caplog.text

    def test_log_with_level(self, caplog):
        from ffbb_api_client_v2.utils.secure_logging import SecureLogger

        sl = SecureLogger("test_log", level=logging.DEBUG)
        with caplog.at_level(logging.WARNING, logger="test_log"):
            sl.log(logging.WARNING, "Custom level msg")
        assert "Custom level msg" in caplog.text


# ---------------------------------------------------------------------------
# RetryUtils coverage (77% → 90%+)
# ---------------------------------------------------------------------------


class TestRetryUtilsCoverage:
    """retry_utils.py — cover calculate_delay jitter, execute_with_retry branches."""

    def test_calculate_delay_with_jitter(self):
        from ffbb_api_client_v2.utils.retry_utils import RetryConfig, calculate_delay

        config = RetryConfig(base_delay=1.0, jitter=True)
        delay = calculate_delay(0, config)
        assert 0.1 <= delay <= 2.0  # base 1.0 ± 25% jitter

    def test_calculate_delay_without_jitter(self):
        from ffbb_api_client_v2.utils.retry_utils import RetryConfig, calculate_delay

        config = RetryConfig(base_delay=1.0, jitter=False)
        delay = calculate_delay(0, config)
        assert delay == 1.0

    def test_calculate_delay_capped_at_max(self):
        from ffbb_api_client_v2.utils.retry_utils import RetryConfig, calculate_delay

        config = RetryConfig(
            base_delay=1.0, max_delay=5.0, jitter=False, backoff_factor=10.0
        )
        delay = calculate_delay(5, config)
        assert delay == 5.0

    @patch("ffbb_api_client_v2.utils.retry_utils.time.sleep")
    def test_execute_with_retry_retries_on_status_code(self, mock_sleep):
        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            execute_with_retry,
        )

        response_429 = MagicMock()
        response_429.status_code = 429
        response_200 = MagicMock()
        response_200.status_code = 200

        func = MagicMock(side_effect=[response_429, response_200])
        config = RetryConfig(max_attempts=2, base_delay=0.01, jitter=False)
        timeout_config = TimeoutConfig()

        result = execute_with_retry(func, config=config, timeout_config=timeout_config)
        assert result.status_code == 200
        assert func.call_count == 2

    @patch("ffbb_api_client_v2.utils.retry_utils.time.sleep")
    def test_execute_with_retry_retries_on_exception(self, mock_sleep):
        import requests

        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            execute_with_retry,
        )

        response_ok = MagicMock()
        response_ok.status_code = 200
        func = MagicMock(side_effect=[requests.ConnectionError("fail"), response_ok])
        config = RetryConfig(max_attempts=2, base_delay=0.01, jitter=False)

        result = execute_with_retry(func, config=config, timeout_config=TimeoutConfig())
        assert result.status_code == 200

    @patch("ffbb_api_client_v2.utils.retry_utils.time.sleep")
    def test_execute_with_retry_exhausted_raises(self, mock_sleep):
        import requests

        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            execute_with_retry,
        )

        func = MagicMock(side_effect=requests.ConnectionError("always fails"))
        config = RetryConfig(max_attempts=1, base_delay=0.01, jitter=False)

        with pytest.raises(requests.ConnectionError):
            execute_with_retry(func, config=config, timeout_config=TimeoutConfig())

    def test_execute_with_retry_preserves_existing_timeout(self):
        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            execute_with_retry,
        )

        response = MagicMock()
        response.status_code = 200
        func = MagicMock(return_value=response)
        config = RetryConfig(max_attempts=0, jitter=False)

        result = execute_with_retry(
            func, config=config, timeout_config=TimeoutConfig(), timeout=99
        )
        assert result.status_code == 200
        # Timeout kwarg should be preserved as 99, not overwritten
        _, kwargs = func.call_args
        assert kwargs["timeout"] == 99

    def test_make_http_request_post(self):
        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            make_http_request_with_retry,
        )

        with patch("requests.Session") as MockSession:
            mock_session = MagicMock()
            response = MagicMock()
            response.status_code = 200
            mock_session.post.return_value = response
            MockSession.return_value = mock_session

            result = make_http_request_with_retry(
                "POST",
                "https://example.com/api",
                {"Content-Type": "application/json"},
                data={"key": "value"},
                retry_config=RetryConfig(max_attempts=0, jitter=False),
                timeout_config=TimeoutConfig(),
            )
            assert result.status_code == 200
            mock_session.post.assert_called_once()

    def test_make_http_request_unsupported_method(self):
        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            make_http_request_with_retry,
        )

        with pytest.raises(ValueError, match="Unsupported HTTP method"):
            make_http_request_with_retry(
                "DELETE",
                "https://example.com/api",
                {},
                retry_config=RetryConfig(max_attempts=0, jitter=False),
                timeout_config=TimeoutConfig(),
            )

    def test_make_http_request_debug_logging(self, caplog):
        from ffbb_api_client_v2.utils.retry_utils import (
            RetryConfig,
            TimeoutConfig,
            make_http_request_with_retry,
        )

        with patch("requests.Session") as MockSession:
            mock_session = MagicMock()
            response = MagicMock()
            response.status_code = 200
            mock_session.get.return_value = response
            MockSession.return_value = mock_session

            make_http_request_with_retry(
                "GET",
                "https://example.com/api",
                {},
                retry_config=RetryConfig(max_attempts=0, jitter=False),
                timeout_config=TimeoutConfig(),
                debug=True,
            )

    def test_create_custom_configs(self):
        from ffbb_api_client_v2.utils.retry_utils import (
            create_custom_retry_config,
            create_custom_timeout_config,
            get_default_retry_config,
            get_default_timeout_config,
        )

        rc = create_custom_retry_config(max_attempts=5, base_delay=2.0, max_delay=30.0)
        assert rc.max_attempts == 5
        assert rc.base_delay == 2.0

        tc = create_custom_timeout_config(connect_timeout=5.0, read_timeout=15.0)
        assert tc.connect_timeout == 5.0
        assert tc.read_timeout == 15.0

        assert get_default_retry_config() is not None
        assert get_default_timeout_config() is not None


# ---------------------------------------------------------------------------
# CacheManager coverage (81% → 90%+)
# ---------------------------------------------------------------------------


class TestCacheManagerCoverage:
    """cache_manager.py — cover edge cases."""

    def setup_method(self):
        from ffbb_api_client_v2.utils.cache_manager import CacheManager

        CacheManager.reset_instance()

    def teardown_method(self):
        from ffbb_api_client_v2.utils.cache_manager import CacheManager

        CacheManager.reset_instance()

    def test_singleton_returns_same_instance(self):
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig, CacheManager

        cm1 = CacheManager(CacheConfig(backend="memory"))
        cm2 = CacheManager()
        assert cm1 is cm2

    def test_clear_cache_no_session(self):
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig, CacheManager

        cm = CacheManager(CacheConfig(enabled=False))
        assert cm.clear_cache() is False

    def test_clear_cache_error(self):
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig, CacheManager

        cm = CacheManager(CacheConfig(backend="memory"))
        cm._session = MagicMock()
        cm._session.cache.clear.side_effect = OSError("disk error")
        assert cm.clear_cache() is False
        assert cm.metrics.errors == 1

    def test_get_cache_size_no_session(self):
        from ffbb_api_client_v2.utils.cache_manager import CacheManager

        CacheManager.reset_instance()
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig

        cm = CacheManager(CacheConfig(enabled=False))
        assert cm.get_cache_size() == 0

    def test_get_cache_size_error(self):
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig, CacheManager

        cm = CacheManager(CacheConfig(backend="memory"))
        cm._session = MagicMock()
        cm._session.cache.count.side_effect = RuntimeError("fail")
        assert cm.get_cache_size() == 0
        assert cm.metrics.errors >= 1

    def test_warm_cache_disabled(self):
        from ffbb_api_client_v2.utils.cache_manager import CacheManager

        CacheManager.reset_instance()
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig

        cm = CacheManager(CacheConfig(enabled=False))
        result = cm.warm_cache(["https://example.com"])
        assert result == 0

    def test_invalidate_pattern_disabled(self):
        from ffbb_api_client_v2.utils.cache_manager import CacheManager

        CacheManager.reset_instance()
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig

        cm = CacheManager(CacheConfig(enabled=False))
        result = cm.invalidate_pattern("test")
        assert result == 0

    def test_invalidate_pattern_with_matching_keys(self):
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig, CacheManager

        cm = CacheManager(CacheConfig(backend="memory"))
        # Mock the session cache with delete and keys
        mock_cache = MagicMock()
        mock_cache.keys.return_value = ["ffbb_api:abc_test_123", "ffbb_api:other_456"]
        cm._session = MagicMock()
        cm._session.cache = mock_cache
        cm.config.enabled = True

        result = cm.invalidate_pattern("test")
        assert result == 1
        mock_cache.delete.assert_called_once_with("ffbb_api:abc_test_123")

    def test_get_metrics(self):
        from ffbb_api_client_v2.utils.cache_manager import CacheConfig, CacheManager

        cm = CacheManager(CacheConfig(backend="memory"))
        metrics = cm.get_metrics()
        assert metrics.hits == 0
        assert metrics.hit_rate == 0.0

    def test_cache_metrics_reset(self):
        from ffbb_api_client_v2.utils.cache_manager import CacheMetrics

        m = CacheMetrics(hits=5, misses=3)
        assert m.hit_rate == 5 / 8
        m.reset()
        assert m.hits == 0
        assert m.misses == 0


# ---------------------------------------------------------------------------
# __init__.py coverage (86% → 90%+)
# ---------------------------------------------------------------------------


class TestInitCoverage:
    """__init__.py — cover PackageNotFoundError branch."""

    def test_version_is_set(self):
        import ffbb_api_client_v2

        assert hasattr(ffbb_api_client_v2, "__version__")
        # In dev, version will be "unknown" since package isn't installed
        assert isinstance(ffbb_api_client_v2.__version__, str)


# ---------------------------------------------------------------------------
# OrganismeIdPere to_dict coverage (83% → 90%+)
# ---------------------------------------------------------------------------


class TestOrganismeIdPereToDictCoverage:
    """organisme_id_pere.py — cover to_dict branches."""

    def test_to_dict_all_fields(self):
        from ffbb_api_client_v2.models.organisme_id_pere import OrganismeIDPere

        data = {
            "adresse": "1 rue de Paris",
            "adresseClubPro": None,
            "cartographie": "some",
            "code": "CL01",
            "commune": "75001",
            "communeClubPro": None,
            "date_created": "2024-01-01T00:00:00",
            "date_updated": "2024-06-01T00:00:00",
            "id": "12345",
            "mail": "club@example.com",
            "nom": "Club Paris",
            "nomClubPro": "Pro Paris",
            "organisme_id_pere": None,
            "salle": None,
            "telephone": "0600000000",
            "type": "Association",
            "type_association": None,
            "urlSiteWeb": "https://club.fr",
            "logo": "550e8400-e29b-41d4-a716-446655440000",
            "nom_simple": "club paris",
            "dateAffiliation": None,
            "saison_en_cours": "true",
            "entreprise": "false",
            "handibasket": "true",
            "omnisport": "false",
            "horsAssociation": "false",
            "offresPratiques": ["basket"],
            "engagements": ["eng1"],
            "labellisation": ["label1"],
        }
        obj = OrganismeIDPere.from_dict(data)
        d = obj.to_dict()
        assert d["adresse"] == "1 rue de Paris"
        assert d["code"] == "CL01"
        assert d["commune"] == "75001"
        assert "date_created" in d
        assert "date_updated" in d
        assert d["id"] == "12345"
        assert d["mail"] == "club@example.com"
        assert d["nom"] == "Club Paris"
        assert d["nomClubPro"] == "Pro Paris"
        assert d["telephone"] == "0600000000"
        assert d["type"] == "Association"
        assert d["urlSiteWeb"] == "https://club.fr"
        assert d["nom_simple"] == "club paris"
        assert d["saison_en_cours"] is True
        assert d["entreprise"] is False
        assert d["handibasket"] is True
        assert d["omnisport"] is False
        assert d["horsAssociation"] is False
        assert d["offresPratiques"] == ["basket"]
        assert d["engagements"] == ["eng1"]
        assert d["labellisation"] == ["label1"]
        assert "logo" in d


# ---------------------------------------------------------------------------
# MultiSearchResultRencontres to_dict coverage (87% → 90%+)
# ---------------------------------------------------------------------------


class TestMultiSearchResultRencontresToDictCoverage:
    """multi_search_result_rencontres.py — cover to_dict branches."""

    def test_rencontres_hit_to_dict_all_fields(self):
        from ffbb_api_client_v2.models.rencontres_hit import RencontresHit

        data = {
            "niveau": "Départemental",
            "id": "r-1",
            "date": "2024-06-15T20:00:00",
            "date_rencontre": "2024-06-15T20:00:00",
            "horaire": "2000",
            "nomEquipe1": "Team A",
            "nomEquipe2": "Team B",
            "numeroJournee": "5",
            "pratique": "5x5",
            "gsId": "gs-123",
            "officiels": ["Ref1"],
            "competitionId": {"code": "NM1"},
            "idOrganismeEquipe1": {"id": "o1", "nom": "Club A"},
            "idOrganismeEquipe2": {"id": "o2", "nom": "Club B"},
            "idPoule": {"id": "p1"},
            "saison": {"code": "2024"},
            "salle": {"libelle": "Salle X", "adresse": "1 rue"},
            "idEngagementEquipe1": {"id": "e1"},
            "idEngagementEquipe2": {"id": "e2"},
            "_geo": {"lat": 48.85, "lng": 2.35},
            "date_timestamp": "1718485200",
            "date_rencontre_timestamp": "1718485200",
            "creation_timestamp": "1718485200",
            "dateSaisieResultat_timestamp": "1718485200",
            "modification_timestamp": "1718485200",
            "thumbnail": None,
            "organisateur": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "nom": "Org1",
            },
            "niveau_nb": "3",
        }
        hit = RencontresHit.from_dict(data)
        d = hit.to_dict()
        assert d["nomEquipe1"] == "Team A"
        assert d["nomEquipe2"] == "Team B"
        assert d["id"] == "r-1"
        assert "date" in d
        assert "date_rencontre" in d
        assert d["horaire"] == "2000"
        assert d["numeroJournee"] == "5"
        assert "competitionId" in d
        assert "idOrganismeEquipe1" in d
        assert "idOrganismeEquipe2" in d
        assert "idPoule" in d
        assert "saison" in d
        assert "salle" in d
        assert "idEngagementEquipe1" in d
        assert "idEngagementEquipe2" in d
        assert "_geo" in d
        assert "date_timestamp" in d
        assert "date_rencontre_timestamp" in d
        assert "creation_timestamp" in d
        assert "dateSaisieResultat_timestamp" in d
        assert "modification_timestamp" in d
        assert "organisateur" in d
        assert d["niveau_nb"] == "3"


# ---------------------------------------------------------------------------
# FFBBAPIClientV2 coverage (88% → 90%+)
# ---------------------------------------------------------------------------


class TestFFBBAPIClientV2Coverage:
    """ffbb_api_client_v2.py — cover search_multiple_* with None names."""

    def test_search_multiple_with_none_names_returns_none(self):
        from ffbb_api_client_v2.clients.ffbb_api_client_v2 import FFBBAPIClientV2

        api_client = MagicMock()
        meili_client = MagicMock()
        client = FFBBAPIClientV2(api_client, meili_client)

        assert client.search_multiple_competitions(None) is None
        assert client.search_multiple_organismes(None) is None
        assert client.search_multiple_pratiques(None) is None
        assert client.search_multiple_rencontres(None) is None
        assert client.search_multiple_salles(None) is None
        assert client.search_multiple_terrains(None) is None
        assert client.search_multiple_tournois(None) is None

    def test_search_multiple_with_empty_list_returns_none(self):
        from ffbb_api_client_v2.clients.ffbb_api_client_v2 import FFBBAPIClientV2

        api_client = MagicMock()
        meili_client = MagicMock()
        client = FFBBAPIClientV2(api_client, meili_client)

        assert client.search_multiple_competitions([]) is None
        assert client.search_multiple_organismes([]) is None

    def test_get_competition_delegates(self):
        from ffbb_api_client_v2.clients.ffbb_api_client_v2 import FFBBAPIClientV2

        api_client = MagicMock()
        api_client.get_competition.return_value = "result"
        meili_client = MagicMock()
        client = FFBBAPIClientV2(api_client, meili_client)

        result = client.get_competition(competition_id=123)
        assert result == "result"
        api_client.get_competition.assert_called_once()

    def test_get_organisme_delegates(self):
        from ffbb_api_client_v2.clients.ffbb_api_client_v2 import FFBBAPIClientV2

        api_client = MagicMock()
        api_client.get_organisme.return_value = "org_result"
        meili_client = MagicMock()
        client = FFBBAPIClientV2(api_client, meili_client)

        result = client.get_organisme(organisme_id=456)
        assert result == "org_result"

    def test_get_poule_delegates(self):
        from ffbb_api_client_v2.clients.ffbb_api_client_v2 import FFBBAPIClientV2

        api_client = MagicMock()
        api_client.get_poule.return_value = "poule_result"
        meili_client = MagicMock()
        client = FFBBAPIClientV2(api_client, meili_client)

        result = client.get_poule(poule_id=789)
        assert result == "poule_result"


# ---------------------------------------------------------------------------
# Additional tests for "False branch" coverage (empty/minimal data)
# These cover the `if self.field is not None:` False paths
# ---------------------------------------------------------------------------


class TestEmptyToDictBranches:
    """Cover the False branches of to_dict (field IS None → skip)."""

    def test_cartographie_empty_to_dict(self):
        from ffbb_api_client_v2.models.cartographie import Cartographie

        c = Cartographie.from_dict(
            {
                "date_created": None,
                "date_updated": None,
            }
        )
        d = c.to_dict()
        assert d == {}

    def test_folder_empty_to_dict(self):
        from ffbb_api_client_v2.models.folder import Folder

        f = Folder.from_dict({"parent": None})
        d = f.to_dict()
        assert d == {}

    def test_document_flyer_minimal_to_dict(self):
        """Test DocumentFlyer to_dict with only None-typed fields skipped."""
        from ffbb_api_client_v2.models.document_flyer import DocumentFlyer

        doc = DocumentFlyer.from_dict(
            {
                "charset": None,
                "duration": None,
                "embed": None,
                "description": None,
                "location": None,
                "tags": None,
                "credits": None,
                "newsbridge_media_id": None,
                "newsbridge_metadatas": None,
                "newsbridge_name": None,
                "newsbridge_recorded_at": None,
                "focal_point_x": None,
                "focal_point_y": None,
                "uploaded_by": None,
                "modified_by": None,
                "newsbridge_mission": None,
            }
        )
        d = doc.to_dict()
        # All None-typed fields → empty dict
        assert d == {}

    def test_organisme_id_pere_with_nested_organisme(self):
        """Cover the organisme_id_pere nested field + more to_dict branches."""
        from ffbb_api_client_v2.models.organisme_id_pere import OrganismeIDPere

        data = {
            "adresse": None,
            "adresseClubPro": None,
            "cartographie": None,
            "code": None,
            "commune": None,
            "communeClubPro": None,
            "date_created": None,
            "date_updated": None,
            "id": None,
            "mail": None,
            "nom": None,
            "nomClubPro": None,
            "organisme_id_pere": {
                "adresse": "nested addr",
                "adresseClubPro": None,
                "cartographie": None,
                "code": "N01",
                "commune": None,
                "communeClubPro": None,
                "date_created": None,
                "date_updated": None,
                "id": "99",
                "mail": None,
                "nom": "Nested Org",
                "nomClubPro": None,
                "organisme_id_pere": None,
                "salle": None,
                "telephone": None,
                "type": None,
                "type_association": None,
                "urlSiteWeb": None,
                "logo": None,
                "nom_simple": None,
                "dateAffiliation": None,
                "saison_en_cours": None,
                "entreprise": None,
                "handibasket": None,
                "omnisport": None,
                "horsAssociation": None,
                "offresPratiques": None,
                "engagements": None,
                "labellisation": None,
            },
            "salle": None,
            "telephone": None,
            "type": None,
            "type_association": None,
            "urlSiteWeb": None,
            "logo": None,
            "nom_simple": None,
            "dateAffiliation": None,
            "saison_en_cours": None,
            "entreprise": None,
            "handibasket": None,
            "omnisport": None,
            "horsAssociation": None,
            "offresPratiques": None,
            "engagements": None,
            "labellisation": None,
        }
        obj = OrganismeIDPere.from_dict(data)
        assert obj.organisme_id_pere is not None
        assert obj.organisme_id_pere.nom == "Nested Org"
        d = obj.to_dict()
        assert "organisme_id_pere" in d
        assert d["organisme_id_pere"]["code"] == "N01"

    def test_organisme_id_pere_empty_to_dict(self):
        """Cover all False branches in OrganismeIDPere.to_dict."""
        from ffbb_api_client_v2.models.organisme_id_pere import OrganismeIDPere

        data = {
            "adresse": None,
            "adresseClubPro": None,
            "cartographie": None,
            "code": None,
            "commune": None,
            "communeClubPro": None,
            "date_created": None,
            "date_updated": None,
            "id": None,
            "mail": None,
            "nom": None,
            "nomClubPro": None,
            "organisme_id_pere": None,
            "salle": None,
            "telephone": None,
            "type": None,
            "type_association": None,
            "urlSiteWeb": None,
            "logo": None,
            "nom_simple": None,
            "dateAffiliation": None,
            "saison_en_cours": None,
            "entreprise": None,
            "handibasket": None,
            "omnisport": None,
            "horsAssociation": None,
            "offresPratiques": None,
            "engagements": None,
            "labellisation": None,
        }
        obj = OrganismeIDPere.from_dict(data)
        d = obj.to_dict()
        assert d == {}

    def test_multi_search_results_to_dict_empty(self):
        """Cover the False branches of MultiSearchResult.to_dict."""
        from ffbb_api_client_v2.models.multi_search_result_organismes import (
            OrganismesMultiSearchResult,
        )

        result = OrganismesMultiSearchResult(
            index_uid=None,
            hits=None,
            query=None,
            processing_time_ms=None,
            limit=None,
            offset=None,
            estimated_total_hits=None,
            facet_distribution=None,
            facet_stats=None,
        )
        d = result.to_dict()
        assert d == {}

    def test_multi_search_results_type_error(self):
        """Cover the TypeError branch in MultiSearchResult.from_dict."""
        from ffbb_api_client_v2.models.multi_search_results import MultiSearchResult

        # MultiSearchResult itself is the generic base — calling from_dict
        # on it directly raises (TypeError or AttributeError)
        with pytest.raises((TypeError, AttributeError)):
            MultiSearchResult.from_dict({"indexUid": "test"})


class TestInitVersionCoverage:
    """__init__.py — cover the PackageNotFoundError branch."""

    def test_version_when_package_not_found(self):
        """The __version__ is either the real version or 'unknown'."""
        import ffbb_api_client_v2

        # In dev without pip install -e, it's 'unknown'
        assert isinstance(ffbb_api_client_v2.__version__, str)
        # Cover the __all__ export
        assert "FFBBAPIClientV2" in ffbb_api_client_v2.__all__
