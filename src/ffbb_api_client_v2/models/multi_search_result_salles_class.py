"""Backward compatibility module for SallesMultiSearchResult."""

from .multi_search_result_salles import (
    SallesFacetDistribution,
    SallesFacetStats,
    SallesHit,
    SallesMultiSearchResult,
)

__all__ = [
    "SallesFacetDistribution",
    "SallesFacetStats",
    "SallesHit",
    "SallesMultiSearchResult",
]
