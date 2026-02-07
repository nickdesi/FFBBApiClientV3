"""
FFBB API Client V2.

A Python client library for the French Basketball Federation (FFBB) API,
providing access to clubs, competitions, matches, and other basketball data.
"""

from .clients.api_ffbb_app_client import ApiFFBBAppClient
from .clients.ffbb_api_client_v2 import FFBBAPIClientV2
from .clients.meilisearch_client import MeilisearchClient
from .clients.meilisearch_ffbb_client import MeilisearchFFBBClient
from .helpers.meilisearch_client_extension import MeilisearchClientExtension
from .helpers.multi_search_query_helper import generate_queries
from .models.multi_search_query import MultiSearchQuery
from .models.multi_search_result_competitions import (
    CompetitionsFacetDistribution,
    CompetitionsFacetStats,
    CompetitionsHit,
    CompetitionsMultiSearchResult,
)
from .models.multi_search_result_organismes import (
    OrganismesFacetDistribution,
    OrganismesFacetStats,
    OrganismesHit,
    OrganismesMultiSearchResult,
)
from .models.multi_search_result_pratiques import (
    PratiquesFacetDistribution,
    PratiquesFacetStats,
    PratiquesHit,
    PratiquesMultiSearchResult,
)
from .models.multi_search_result_rencontres import (
    RencontresFacetDistribution,
    RencontresFacetStats,
    RencontresHit,
    RencontresMultiSearchResult,
)
from .models.multi_search_result_salles import (
    SallesFacetDistribution,
    SallesFacetStats,
    SallesHit,
    SallesMultiSearchResult,
)
from .models.multi_search_result_terrains import (
    TerrainsFacetDistribution,
    TerrainsFacetStats,
    TerrainsHit,
    TerrainsMultiSearchResult,
)
from .models.multi_search_result_tournois import (
    TournoisFacetDistribution,
    TournoisFacetStats,
    TournoisHit,
    TournoisMultiSearchResult,
)
from .utils.token_manager import FFBBTokens, TokenManager

# Public API exports
__all__ = [
    # Clients
    "ApiFFBBAppClient",
    "FFBBAPIClientV2",
    "MeilisearchClient",
    "MeilisearchFFBBClient",
    # Helpers
    "MeilisearchClientExtension",
    "generate_queries",
    # Query
    "MultiSearchQuery",
    # Competitions
    "CompetitionsFacetDistribution",
    "CompetitionsFacetStats",
    "CompetitionsHit",
    "CompetitionsMultiSearchResult",
    # Organismes
    "OrganismesFacetDistribution",
    "OrganismesFacetStats",
    "OrganismesHit",
    "OrganismesMultiSearchResult",
    # Pratiques
    "PratiquesFacetDistribution",
    "PratiquesFacetStats",
    "PratiquesHit",
    "PratiquesMultiSearchResult",
    # Rencontres
    "RencontresFacetDistribution",
    "RencontresFacetStats",
    "RencontresHit",
    "RencontresMultiSearchResult",
    # Salles
    "SallesFacetDistribution",
    "SallesFacetStats",
    "SallesHit",
    "SallesMultiSearchResult",
    # Terrains
    "TerrainsFacetDistribution",
    "TerrainsFacetStats",
    "TerrainsHit",
    "TerrainsMultiSearchResult",
    # Tournois
    "TournoisFacetDistribution",
    "TournoisFacetStats",
    "TournoisHit",
    "TournoisMultiSearchResult",
    # Token management
    "FFBBTokens",
    "TokenManager",
]

from importlib.metadata import PackageNotFoundError, version

try:
    DIST_NAME = __name__
    __version__ = version(DIST_NAME)
except PackageNotFoundError:
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
