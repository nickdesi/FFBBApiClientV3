from __future__ import annotations

from .multi_search_results import MultiSearchResult
from .tournois_facet_distribution import TournoisFacetDistribution
from .tournois_facet_stats import TournoisFacetStats
from .tournois_hit import TournoisHit


class TournoisMultiSearchResult(
    MultiSearchResult[TournoisHit, TournoisFacetDistribution, TournoisFacetStats]
):
    """MultiSearchResult for Tournois."""
