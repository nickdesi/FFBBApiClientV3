from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..utils.converter_utils import (
    from_int,
    from_list,
    from_str,
)
from .facet_distribution import FacetDistribution
from .facet_stats import FacetStats
from .hit import Hit
from .multi_search_results import MultiSearchResult


@dataclass
class MultiSearchQuery:
    index_uid: str | None = None
    q: str | None = None
    facets: list[str] | None = None
    limit: int | None = 10
    offset: int | None = 0
    filter: list[Any] | None = None
    sort: list[Any] | None = None
    lower_q: str | None = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self.lower_q = self.q.lower() if self.q else None

    @staticmethod
    def from_dict(obj: Any) -> MultiSearchQuery:
        assert isinstance(obj, dict)
        index_uid = from_str(obj, "indexUid")
        q = from_str(obj, "q")
        facets = from_list(str, obj, "facets")
        limit = from_int(obj, "limit")
        offset = from_int(obj, "offset")
        filter = from_list(lambda x: x, obj, "filter")
        sort = from_list(lambda x: x, obj, "sort")
        return MultiSearchQuery(
            index_uid=index_uid,
            q=q,
            facets=facets,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.index_uid is not None:
            result["indexUid"] = self.index_uid
        if self.q is not None:
            result["q"] = self.q
        if self.facets is not None:
            result["facets"] = self.facets
        if self.limit is not None:
            result["limit"] = self.limit
        if self.offset is not None:
            result["offset"] = self.offset
        if self.filter is not None:
            result["filter"] = self.filter
        if self.sort is not None:
            result["sort"] = self.sort
        return result

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, MultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, FacetDistribution)
            )
            and (
                result.facet_stats is None or isinstance(result.facet_stats, FacetStats)
            )
        )

    def is_valid_hit(self, _hit: Hit):
        return True

    def filter_result(self, result: MultiSearchResult) -> MultiSearchResult:
        if self.lower_q and result.hits:
            invalid_hits = [
                hit for hit in result.hits if not hit.is_valid_for_query(self.lower_q)
            ]

            if invalid_hits:
                if result.estimated_total_hits is not None:
                    result.estimated_total_hits -= len(invalid_hits)

                for hit in invalid_hits:
                    result.hits.remove(hit)
        return result
