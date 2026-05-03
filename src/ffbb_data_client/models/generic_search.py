from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from .facet_distribution import FacetDistribution
from .facet_stats import FacetStats
from .hit import Hit
from .multi_search_results import MultiSearchResult


@dataclass
class GenericSearchHit(Hit):
    """Meilisearch hit for content indexes whose schema changes frequently."""

    data: dict[str, Any] = field(default_factory=dict)

    @property
    def id(self) -> Any | None:
        return self.data.get("id")

    @property
    def title(self) -> str | None:
        title = self.data.get("title")
        return str(title) if title is not None else None

    @property
    def type(self) -> str | None:
        value = self.data.get("type")
        return str(value) if value is not None else None

    @staticmethod
    def from_dict(obj: Any) -> GenericSearchHit:
        return GenericSearchHit(data=dict(obj) if isinstance(obj, dict) else {})

    def to_dict(self) -> dict[str, Any]:
        return dict(self.data)

    def is_valid_for_query(self, query: str) -> bool:
        if not query:
            return True
        haystack = json.dumps(self.data, ensure_ascii=False, default=str).lower()
        return query.lower() in haystack


@dataclass
class GenericFacetDistribution(FacetDistribution):
    data: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_dict(obj: Any) -> GenericFacetDistribution:
        return GenericFacetDistribution(data=dict(obj) if isinstance(obj, dict) else {})

    def to_dict(self) -> dict[str, Any]:
        return dict(self.data)


@dataclass
class GenericFacetStats(FacetStats):
    data: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_dict(obj: Any) -> GenericFacetStats:
        return GenericFacetStats(data=dict(obj) if isinstance(obj, dict) else {})

    def to_dict(self) -> dict[str, Any]:
        return dict(self.data)


class NewsMultiSearchResult(
    MultiSearchResult[GenericSearchHit, GenericFacetDistribution, GenericFacetStats]
):
    """MultiSearchResult for ffbbsite_news."""


class YoutubeVideosMultiSearchResult(
    MultiSearchResult[GenericSearchHit, GenericFacetDistribution, GenericFacetStats]
):
    """MultiSearchResult for youtube_videos."""


class RssMultiSearchResult(
    MultiSearchResult[GenericSearchHit, GenericFacetDistribution, GenericFacetStats]
):
    """MultiSearchResult for ffbbnational_rss."""


class GaleriesMultiSearchResult(
    MultiSearchResult[GenericSearchHit, GenericFacetDistribution, GenericFacetStats]
):
    """MultiSearchResult for ffbbnational_galeries."""
