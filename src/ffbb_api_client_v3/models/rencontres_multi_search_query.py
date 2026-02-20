from __future__ import annotations

from ..config import MEILISEARCH_FACETS_RENCONTRES, MEILISEARCH_INDEX_RENCONTRES
from .multi_search_query import MultiSearchQuery
from .multi_search_result_rencontres import RencontresMultiSearchResult
from .multi_search_results import MultiSearchResult
from .rencontres_facet_distribution import RencontresFacetDistribution
from .rencontres_facet_stats import RencontresFacetStats


class RencontresMultiSearchQuery(MultiSearchQuery):
    def __init__(
        self,
        q: str | None,
        limit: int | None = 10,
        offset: int | None = 0,
        filter: list[str] | None = None,
        sort: list[str] | None = None,
    ):
        super().__init__(
            index_uid=MEILISEARCH_INDEX_RENCONTRES,
            q=q,
            facets=MEILISEARCH_FACETS_RENCONTRES,
            limit=limit,
            offset=offset,
            filter=filter,
            sort=sort,
        )

    def is_valid_result(self, result: MultiSearchResult):
        return result and (
            isinstance(result, RencontresMultiSearchResult)
            and (
                result.facet_distribution is None
                or isinstance(result.facet_distribution, RencontresFacetDistribution)
            )
            and (
                result.facet_stats is None
                or isinstance(result.facet_stats, RencontresFacetStats)
            )
        )
