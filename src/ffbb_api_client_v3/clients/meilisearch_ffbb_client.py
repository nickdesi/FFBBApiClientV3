from __future__ import annotations

from typing import cast

from httpx import Client

from ..config import MEILISEARCH_BASE_URL
from ..helpers.meilisearch_client_extension import MeilisearchClientExtension
from ..models.competitions_multi_search_query import CompetitionsMultiSearchQuery
from ..models.multi_search_result_competitions import CompetitionsMultiSearchResult
from ..models.multi_search_result_organismes import OrganismesMultiSearchResult
from ..models.multi_search_result_pratiques import PratiquesMultiSearchResult
from ..models.multi_search_result_rencontres import RencontresMultiSearchResult
from ..models.multi_search_result_salles import SallesMultiSearchResult
from ..models.multi_search_result_terrains import TerrainsMultiSearchResult
from ..models.multi_search_result_tournois import TournoisMultiSearchResult
from ..models.organismes_multi_search_query import OrganismesMultiSearchQuery
from ..models.pratiques_multi_search_query import PratiquesMultiSearchQuery
from ..models.rencontres_multi_search_query import RencontresMultiSearchQuery
from ..models.salles_multi_search_query import SallesMultiSearchQuery
from ..models.terrains_multi_search_query import TerrainsMultiSearchQuery
from ..models.tournois_multi_search_query import TournoisMultiSearchQuery


class MeilisearchFFBBClient(MeilisearchClientExtension):
    def __init__(
        self,
        bearer_token: str,
        url: str = MEILISEARCH_BASE_URL,
        debug: bool = False,
        cached_session: Client | None = None,
        async_cached_session: httpx.AsyncClient | None = None,
    ):
        super().__init__(bearer_token, url, debug, cached_session, async_cached_session)

    def search_multiple_organismes(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[OrganismesMultiSearchResult] | None:
        if not names:
            return None

        queries = [OrganismesMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[OrganismesMultiSearchResult], results.results)
            if results
            else None
        )

    def search_organismes(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> OrganismesMultiSearchResult | None:
        results = self.search_multiple_organismes([name], cached_session)
        return results[0] if results else None

    def search_multiple_rencontres(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[RencontresMultiSearchResult] | None:
        if not names:
            return None

        queries = [RencontresMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[RencontresMultiSearchResult], results.results)
            if results
            else None
        )

    def search_rencontres(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> RencontresMultiSearchResult | None:
        results = self.search_multiple_rencontres([name], cached_session)
        return results[0] if results else None

    def search_multiple_terrains(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[TerrainsMultiSearchResult] | None:
        if not names:
            return None

        queries = [TerrainsMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[TerrainsMultiSearchResult], results.results) if results else None
        )

    def search_terrains(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> TerrainsMultiSearchResult | None:
        results = self.search_multiple_terrains([name], cached_session)
        return results[0] if results else None

    def search_multiple_competitions(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[CompetitionsMultiSearchResult] | None:
        if not names:
            return None

        queries = [CompetitionsMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[CompetitionsMultiSearchResult], results.results)
            if results
            else None
        )

    def search_competitions(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> CompetitionsMultiSearchResult | None:
        results = self.search_multiple_competitions([name], cached_session)
        return results[0] if results else None

    def search_multiple_salles(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[SallesMultiSearchResult] | None:
        if not names:
            return None

        queries = [SallesMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

        return cast(list[SallesMultiSearchResult], results.results) if results else None

    def search_salles(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> SallesMultiSearchResult | None:
        results = self.search_multiple_salles([name], cached_session)
        return results[0] if results else None

    def search_multiple_tournois(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[TournoisMultiSearchResult] | None:
        if not names:
            return None

        queries = [TournoisMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[TournoisMultiSearchResult], results.results) if results else None
        )

    def search_tournois(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> TournoisMultiSearchResult | None:
        results = self.search_multiple_tournois([name], cached_session)
        return results[0] if results else None

    def search_multiple_pratiques(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[PratiquesMultiSearchResult] | None:
        if not names:
            return None

        queries = [PratiquesMultiSearchQuery(name) for name in names]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[PratiquesMultiSearchResult], results.results) if results else None
        )

    def search_pratiques(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> PratiquesMultiSearchResult | None:
        results = self.search_multiple_pratiques([name], cached_session)
        return results[0] if results else None
