from __future__ import annotations

from ..config import (
    MEILISEARCH_FACETS_GALERIES,
    MEILISEARCH_FACETS_NEWS,
    MEILISEARCH_FACETS_RSS,
    MEILISEARCH_FACETS_YOUTUBE_VIDEOS,
    MEILISEARCH_INDEX_GALERIES,
    MEILISEARCH_INDEX_NEWS,
    MEILISEARCH_INDEX_RSS,
    MEILISEARCH_INDEX_YOUTUBE_VIDEOS,
)
from .multi_search_query import MultiSearchQuery


class NewsMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
    ):
        super().__init__(
            index_uid=MEILISEARCH_INDEX_NEWS,
            q=q,
            facets=MEILISEARCH_FACETS_NEWS,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )


class YoutubeVideosMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
    ):
        super().__init__(
            index_uid=MEILISEARCH_INDEX_YOUTUBE_VIDEOS,
            q=q,
            facets=MEILISEARCH_FACETS_YOUTUBE_VIDEOS,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )


class RssMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
    ):
        super().__init__(
            index_uid=MEILISEARCH_INDEX_RSS,
            q=q,
            facets=MEILISEARCH_FACETS_RSS,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )


class GaleriesMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
    ):
        super().__init__(
            index_uid=MEILISEARCH_INDEX_GALERIES,
            q=q,
            facets=MEILISEARCH_FACETS_GALERIES,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )
