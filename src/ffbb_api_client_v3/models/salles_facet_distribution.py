from __future__ import annotations

from typing import Any

from .facet_distribution import FacetDistribution


class SallesFacetDistribution(FacetDistribution):
    @staticmethod
    def from_dict(obj: Any) -> SallesFacetDistribution:
        return SallesFacetDistribution()

    def to_dict(self) -> dict:
        return super().to_dict()
