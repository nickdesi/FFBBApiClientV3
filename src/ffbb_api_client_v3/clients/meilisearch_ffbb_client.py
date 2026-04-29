from __future__ import annotations

from typing import cast

import httpx
from httpx import Client

from ..config import MEILISEARCH_BASE_URL
from ..helpers.meilisearch_client_extension import MeilisearchClientExtension
from ..models.competitions_multi_search_query import CompetitionsMultiSearchQuery
from ..models.content_multi_search_query import (
    GaleriesMultiSearchQuery,
    NewsMultiSearchQuery,
    RssMultiSearchQuery,
    YoutubeVideosMultiSearchQuery,
)
from ..models.engagements_multi_search_query import EngagementsMultiSearchQuery
from ..models.formations_multi_search_query import FormationsMultiSearchQuery
from ..models.generic_search import (
    GaleriesMultiSearchResult,
    NewsMultiSearchResult,
    RssMultiSearchResult,
    YoutubeVideosMultiSearchResult,
)
from ..models.multi_search_result_competitions import CompetitionsMultiSearchResult
from ..models.multi_search_result_engagements import EngagementsMultiSearchResult
from ..models.multi_search_result_formations import FormationsMultiSearchResult
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
        *,
        async_cached_session: httpx.AsyncClient | None = None,
    ):
        super().__init__(
            bearer_token,
            url,
            debug,
            cached_session,
            async_cached_session=async_cached_session,
        )

    def search_multiple_organismes(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> list[OrganismesMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            OrganismesMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[OrganismesMultiSearchResult], results.results)
            if results
            else None
        )

    def search_organismes(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> OrganismesMultiSearchResult | None:
        results = self.search_multiple_organismes(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_multiple_rencontres(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> list[RencontresMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            RencontresMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[RencontresMultiSearchResult], results.results)
            if results
            else None
        )

    def search_rencontres(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> RencontresMultiSearchResult | None:
        results = self.search_multiple_rencontres(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_multiple_terrains(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> list[TerrainsMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            TerrainsMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[TerrainsMultiSearchResult], results.results) if results else None
        )

    def search_terrains(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> TerrainsMultiSearchResult | None:
        results = self.search_multiple_terrains(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_multiple_competitions(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> list[CompetitionsMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            CompetitionsMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[CompetitionsMultiSearchResult], results.results)
            if results
            else None
        )

    def search_competitions(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> CompetitionsMultiSearchResult | None:
        results = self.search_multiple_competitions(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_multiple_salles(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> list[SallesMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            SallesMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return cast(list[SallesMultiSearchResult], results.results) if results else None

    def search_salles(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> SallesMultiSearchResult | None:
        results = self.search_multiple_salles(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_multiple_tournois(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> list[TournoisMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            TournoisMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[TournoisMultiSearchResult], results.results) if results else None
        )

    def search_tournois(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> TournoisMultiSearchResult | None:
        results = self.search_multiple_tournois(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_multiple_pratiques(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> list[PratiquesMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            PratiquesMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[PratiquesMultiSearchResult], results.results) if results else None
        )

    def search_pratiques(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> PratiquesMultiSearchResult | None:
        results = self.search_multiple_pratiques(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_multiple_engagements(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> list[EngagementsMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            EngagementsMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[EngagementsMultiSearchResult], results.results)
            if results
            else None
        )

    def search_engagements(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> EngagementsMultiSearchResult | None:
        results = self.search_multiple_engagements(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_multiple_formations(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> list[FormationsMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            FormationsMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)

        return (
            cast(list[FormationsMultiSearchResult], results.results)
            if results
            else None
        )

    def search_formations(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> FormationsMultiSearchResult | None:
        results = self.search_multiple_formations(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_multiple_news(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> list[NewsMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            NewsMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)
        return cast(list[NewsMultiSearchResult], results.results) if results else None

    def search_news(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> NewsMultiSearchResult | None:
        results = self.search_multiple_news(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_multiple_youtube_videos(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> list[YoutubeVideosMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            YoutubeVideosMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)
        return (
            cast(list[YoutubeVideosMultiSearchResult], results.results)
            if results
            else None
        )

    def search_youtube_videos(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> YoutubeVideosMultiSearchResult | None:
        results = self.search_multiple_youtube_videos(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_multiple_rss(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> list[RssMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            RssMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)
        return cast(list[RssMultiSearchResult], results.results) if results else None

    def search_rss(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> RssMultiSearchResult | None:
        results = self.search_multiple_rss(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None

    def search_multiple_galeries(
        self,
        names: list[str | None] | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> list[GaleriesMultiSearchResult] | None:
        if not names:
            return None

        queries = [
            GaleriesMultiSearchQuery(name, limit=limit, filter=filter, sort=sort)
            for name in names
        ]
        results = self.recursive_multi_search(queries, cached_session)
        return (
            cast(list[GaleriesMultiSearchResult], results.results) if results else None
        )

    def search_galeries(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
        limit: int | None = 10,
        cached_session: Client | None = None,
    ) -> GaleriesMultiSearchResult | None:
        results = self.search_multiple_galeries(
            [name],
            filter=filter,
            sort=sort,
            limit=limit,
            cached_session=cached_session,
        )
        return results[0] if results else None
