from __future__ import annotations

from typing import Any, Generic, TypeVar, get_args

from ..utils.converter_utils import (
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
)
from .facet_distribution import FacetDistribution
from .facet_stats import FacetStats
from .hit import Hit

HitType = TypeVar("HitType", bound=Hit)
FacetDistributionType = TypeVar("FacetDistributionType", bound=FacetDistribution)
FacetStatsType = TypeVar("FacetStatsType", bound=FacetStats)


class MultiSearchResult(Generic[HitType, FacetDistributionType, FacetStatsType]):
    index_uid: str | None = None
    hits: list[HitType] | None = None
    query: str | None = None
    processing_time_ms: int | None = None
    limit: int | None = None
    offset: int | None = None
    estimated_total_hits: int | None = None
    facet_distribution: FacetDistributionType | None = None
    facet_stats: FacetStatsType | None = None

    def __init__(
        self,
        index_uid: str | None,
        hits: list[HitType] | None,
        query: str | None,
        processing_time_ms: int | None,
        limit: int | None,
        offset: int | None,
        estimated_total_hits: int | None,
        facet_distribution: FacetDistributionType | None,
        facet_stats: FacetStatsType | None,
    ) -> None:
        self.index_uid = index_uid
        self.hits = hits
        self.query = query
        self.processing_time_ms = processing_time_ms
        self.limit = limit
        self.offset = offset
        self.estimated_total_hits = estimated_total_hits
        self.facet_distribution = facet_distribution
        self.facet_stats = facet_stats

    @classmethod
    def from_dict(
        cls,
        obj: Any,
    ) -> MultiSearchResult[HitType, FacetDistributionType, FacetStatsType]:
        """
        Parse dict into the concrete MultiSearchResult subclass.
        Types are extracted from the class's generic parameters.
        """
        assert isinstance(obj, dict)

        # Extract generic type arguments from class definition
        # e.g., OrganismesMultiSearchResult inherits from
        # MultiSearchResult[OrganismesHit, OrganismesFacetDistribution, OrganismesFacetStats]
        orig_bases = getattr(cls, "__orig_bases__", ())
        if not orig_bases:
            raise TypeError(f"{cls.__name__} must be a generic subclass")
        type_args = get_args(orig_bases[0])
        hit_type: type[HitType] = type_args[0]
        facet_distribution_type: type[FacetDistributionType] = type_args[1]
        facet_stats_type: type[FacetStatsType] = type_args[2]

        index_uid = from_union([from_str, from_none], obj.get("indexUid"))
        hits = from_union(
            [lambda x: from_list(hit_type.from_dict, x), from_none], obj.get("hits")
        )
        query = from_union([from_str, from_none], obj.get("query"))
        processing_time_ms = from_union(
            [from_int, from_none], obj.get("processingTimeMs")
        )
        limit = from_union([from_int, from_none], obj.get("limit"))
        offset = from_union([from_int, from_none], obj.get("offset"))
        estimated_total_hits = from_union(
            [from_int, from_none], obj.get("estimatedTotalHits")
        )
        facet_distribution = from_union(
            [facet_distribution_type.from_dict, from_none], obj.get("facetDistribution")
        )
        facet_stats = from_union(
            [facet_stats_type.from_dict, from_none], obj.get("facetStats")
        )
        return cls(
            index_uid,
            hits,
            query,
            processing_time_ms,
            limit,
            offset,
            estimated_total_hits,
            facet_distribution,
            facet_stats,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.index_uid is not None:
            result["indexUid"] = from_union([from_str, from_none], self.index_uid)
        if self.hits is not None:
            result["hits"] = from_union(
                [lambda x: from_list(lambda hit: hit.to_dict(), x), from_none],
                self.hits,
            )
        if self.query is not None:
            result["query"] = from_union([from_str, from_none], self.query)
        if self.processing_time_ms is not None:
            result["processingTimeMs"] = from_union(
                [from_int, from_none], self.processing_time_ms
            )
        if self.limit is not None:
            result["limit"] = from_union([from_int, from_none], self.limit)
        if self.offset is not None:
            result["offset"] = from_union([from_int, from_none], self.offset)
        if self.estimated_total_hits is not None:
            result["estimatedTotalHits"] = from_union(
                [from_int, from_none], self.estimated_total_hits
            )
        if self.facet_distribution is not None:
            result["facetDistribution"] = from_union(
                [lambda x: x.to_dict() if x else {}, from_none],
                self.facet_distribution,
            )
        if self.facet_stats is not None:
            result["facetStats"] = from_union(
                [lambda x: x.to_dict() if x else {}, from_none], self.facet_stats
            )
        return result
