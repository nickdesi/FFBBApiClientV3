from __future__ import annotations

from .competitions_facet_distribution import CompetitionsFacetDistribution
from .competitions_facet_stats import CompetitionsFacetStats
from .competitions_hit import CompetitionsHit
from .multi_search_results import MultiSearchResult


class CompetitionsMultiSearchResult(
    MultiSearchResult[
        CompetitionsHit, CompetitionsFacetDistribution, CompetitionsFacetStats
    ]
):
    """MultiSearchResult for Competitions."""
