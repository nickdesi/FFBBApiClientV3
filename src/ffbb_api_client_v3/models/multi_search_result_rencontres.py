from __future__ import annotations

from .multi_search_results import MultiSearchResult
from .rencontres_facet_distribution import RencontresFacetDistribution
from .rencontres_facet_stats import RencontresFacetStats
from .rencontres_hit import RencontresHit


class RencontresMultiSearchResult(
    MultiSearchResult[RencontresHit, RencontresFacetDistribution, RencontresFacetStats]
):
    """MultiSearchResult for Rencontres."""
