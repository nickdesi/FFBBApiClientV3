"""Tests for MeilisearchFFBBClient search methods."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from ffbb_api_client_v3.clients.meilisearch_ffbb_client import MeilisearchFFBBClient
from ffbb_api_client_v3.models.competitions_multi_search_query import (
    CompetitionsMultiSearchQuery,
)
from ffbb_api_client_v3.models.engagements_multi_search_query import (
    EngagementsMultiSearchQuery,
)
from ffbb_api_client_v3.models.formations_multi_search_query import (
    FormationsMultiSearchQuery,
)
from ffbb_api_client_v3.models.multi_search_result_competitions import (
    CompetitionsMultiSearchResult,
)
from ffbb_api_client_v3.models.multi_search_result_engagements import (
    EngagementsMultiSearchResult,
)
from ffbb_api_client_v3.models.multi_search_result_formations import (
    FormationsMultiSearchResult,
)
from ffbb_api_client_v3.models.multi_search_result_organismes import (
    OrganismesMultiSearchResult,
)
from ffbb_api_client_v3.models.multi_search_result_pratiques import (
    PratiquesMultiSearchResult,
)
from ffbb_api_client_v3.models.multi_search_result_rencontres import (
    RencontresMultiSearchResult,
)
from ffbb_api_client_v3.models.multi_search_result_salles import (
    SallesMultiSearchResult,
)
from ffbb_api_client_v3.models.multi_search_result_terrains import (
    TerrainsMultiSearchResult,
)
from ffbb_api_client_v3.models.multi_search_result_tournois import (
    TournoisMultiSearchResult,
)
from ffbb_api_client_v3.models.multi_search_results_class import MultiSearchResults
from ffbb_api_client_v3.models.organismes_multi_search_query import (
    OrganismesMultiSearchQuery,
)
from ffbb_api_client_v3.models.pratiques_multi_search_query import (
    PratiquesMultiSearchQuery,
)
from ffbb_api_client_v3.models.rencontres_multi_search_query import (
    RencontresMultiSearchQuery,
)
from ffbb_api_client_v3.models.salles_multi_search_query import SallesMultiSearchQuery
from ffbb_api_client_v3.models.terrains_multi_search_query import (
    TerrainsMultiSearchQuery,
)
from ffbb_api_client_v3.models.tournois_multi_search_query import (
    TournoisMultiSearchQuery,
)


class Test040MeilisearchFfbbClient(unittest.TestCase):
    """Tests for MeilisearchFFBBClient search_multiple_* and search_* methods."""

    def setUp(self) -> None:
        with patch("ffbb_api_client_v3.clients.meilisearch_client.CacheManager"):
            self.client = MeilisearchFFBBClient(bearer_token="test-token")

    def _make_mock_results(self, result_mock: MagicMock) -> MultiSearchResults:
        """Create a MultiSearchResults with a single mock result."""
        results = MagicMock(spec=MultiSearchResults)
        results.results = [result_mock]
        return results

    # -- None input tests ------------------------------------------------

    def test_001_search_multiple_organismes_none(self) -> None:
        result = self.client.search_multiple_organismes(None)
        self.assertIsNone(result)

    def test_002_search_multiple_rencontres_none(self) -> None:
        result = self.client.search_multiple_rencontres(None)
        self.assertIsNone(result)

    def test_003_search_multiple_terrains_none(self) -> None:
        result = self.client.search_multiple_terrains(None)
        self.assertIsNone(result)

    def test_004_search_multiple_competitions_none(self) -> None:
        result = self.client.search_multiple_competitions(None)
        self.assertIsNone(result)

    def test_005_search_multiple_salles_none(self) -> None:
        result = self.client.search_multiple_salles(None)
        self.assertIsNone(result)

    def test_006_search_multiple_tournois_none(self) -> None:
        result = self.client.search_multiple_tournois(None)
        self.assertIsNone(result)

    def test_007_search_multiple_pratiques_none(self) -> None:
        result = self.client.search_multiple_pratiques(None)
        self.assertIsNone(result)

    def test_007a_search_multiple_engagements_none(self) -> None:
        result = self.client.search_multiple_engagements(None)
        self.assertIsNone(result)

    def test_007b_search_multiple_formations_none(self) -> None:
        result = self.client.search_multiple_formations(None)
        self.assertIsNone(result)

    # -- Mocked result tests ---------------------------------------------

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_008_search_multiple_organismes_results(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=OrganismesMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_multiple_organismes(["Paris"])
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # type: ignore[arg-type]
        self.assertIsInstance(mock_rms.call_args[0][0][0], OrganismesMultiSearchQuery)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_009_search_multiple_rencontres_results(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=RencontresMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_multiple_rencontres(["Paris"])
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # type: ignore[arg-type]
        self.assertIsInstance(mock_rms.call_args[0][0][0], RencontresMultiSearchQuery)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_010_search_multiple_terrains_results(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=TerrainsMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_multiple_terrains(["Paris"])
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # type: ignore[arg-type]
        self.assertIsInstance(mock_rms.call_args[0][0][0], TerrainsMultiSearchQuery)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_011_search_multiple_competitions_results(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=CompetitionsMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_multiple_competitions(["Paris"])
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # type: ignore[arg-type]
        self.assertIsInstance(mock_rms.call_args[0][0][0], CompetitionsMultiSearchQuery)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_012_search_multiple_salles_results(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=SallesMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_multiple_salles(["Paris"])
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # type: ignore[arg-type]
        self.assertIsInstance(mock_rms.call_args[0][0][0], SallesMultiSearchQuery)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_013_search_multiple_tournois_results(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=TournoisMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_multiple_tournois(["Paris"])
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # type: ignore[arg-type]
        self.assertIsInstance(mock_rms.call_args[0][0][0], TournoisMultiSearchQuery)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_014_search_multiple_pratiques_results(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=PratiquesMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_multiple_pratiques(["basket"])
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # type: ignore[arg-type]
        self.assertIsInstance(mock_rms.call_args[0][0][0], PratiquesMultiSearchQuery)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_014a_search_multiple_engagements_results(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=EngagementsMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_multiple_engagements(["Paris"])
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # type: ignore[arg-type]
        self.assertIsInstance(mock_rms.call_args[0][0][0], EngagementsMultiSearchQuery)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_014b_search_multiple_formations_results(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=FormationsMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_multiple_formations(["Paris"])
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # type: ignore[arg-type]
        self.assertIsInstance(mock_rms.call_args[0][0][0], FormationsMultiSearchQuery)

    # -- Singular delegate tests -----------------------------------------

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_015_search_organismes_result(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=OrganismesMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_organismes("Paris")
        self.assertIsNotNone(result)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_016_search_rencontres_result(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=RencontresMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_rencontres("Paris")
        self.assertIsNotNone(result)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_017_search_terrains_result(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=TerrainsMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_terrains("Paris")
        self.assertIsNotNone(result)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_018_search_competitions_result(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=CompetitionsMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_competitions("Paris")
        self.assertIsNotNone(result)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_019_search_salles_result(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=SallesMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_salles("Paris")
        self.assertIsNotNone(result)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_020_search_tournois_result(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=TournoisMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_tournois("Paris")
        self.assertIsNotNone(result)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_021_search_pratiques_result(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=PratiquesMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_pratiques("basket")
        self.assertIsNotNone(result)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_022_search_engagements_result(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=EngagementsMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_engagements("Paris")
        self.assertIsNotNone(result)

    @patch.object(MeilisearchFFBBClient, "recursive_multi_search")
    def test_023_search_formations_result(self, mock_rms: MagicMock) -> None:
        mock_result = MagicMock(spec=FormationsMultiSearchResult)
        mock_rms.return_value = self._make_mock_results(mock_result)
        result = self.client.search_formations("Paris")
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
