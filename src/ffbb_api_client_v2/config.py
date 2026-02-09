"""Centralized configuration for FFBB API client."""

# API URLs
API_FFBB_BASE_URL = "https://api.ffbb.app/"
MEILISEARCH_BASE_URL = "https://meilisearch-prod.ffbb.app/"

# HTTP Headers
DEFAULT_USER_AGENT = "okhttp/4.12.0"

# Environment variable names for tokens
ENV_API_TOKEN = "API_FFBB_APP_BEARER_TOKEN"
ENV_MEILISEARCH_TOKEN = "MEILISEARCH_BEARER_TOKEN"

# API Endpoint Paths (relative to base URL)
ENDPOINT_CONFIGURATION = "items/configuration"
ENDPOINT_LIVES = "json/lives.json"
ENDPOINT_COMPETITIONS = "items/ffbbserver_competitions"
ENDPOINT_POULES = "items/ffbbserver_poules"
ENDPOINT_SAISONS = "items/ffbbserver_saisons"
ENDPOINT_ORGANISMES = "items/ffbbserver_organismes"

# Meilisearch Endpoint Paths
MEILISEARCH_ENDPOINT_MULTI_SEARCH = "multi-search"

# Meilisearch Index UIDs
MEILISEARCH_INDEX_ORGANISMES = "ffbbserver_organismes"
MEILISEARCH_INDEX_RENCONTRES = "ffbbserver_rencontres"
MEILISEARCH_INDEX_TERRAINS = "ffbbserver_terrains"
MEILISEARCH_INDEX_SALLES = "ffbbserver_salles"
MEILISEARCH_INDEX_TOURNOIS = "ffbbserver_tournois"
MEILISEARCH_INDEX_COMPETITIONS = "ffbbserver_competitions"
MEILISEARCH_INDEX_PRATIQUES = "ffbbnational_pratiques"

MEILISEARCH_INDEX_UIDS = [
    MEILISEARCH_INDEX_ORGANISMES,
    MEILISEARCH_INDEX_RENCONTRES,
    MEILISEARCH_INDEX_TERRAINS,
    MEILISEARCH_INDEX_SALLES,
    MEILISEARCH_INDEX_TOURNOIS,
    MEILISEARCH_INDEX_COMPETITIONS,
    MEILISEARCH_INDEX_PRATIQUES,
]

# Meilisearch Default Facets per Index
MEILISEARCH_FACETS_ORGANISMES = [
    "type_association.libelle",
    "type",
    "labellisation",
    "offresPratiques",
]
MEILISEARCH_FACETS_RENCONTRES = [
    "competitionId.categorie.code",
    "competitionId.typeCompetition",
    "niveau",
    "competitionId.sexe",
    "organisateur.nom",
    "organisateur.id",
    "competitionId.nomExtended",
]
MEILISEARCH_FACETS_TOURNOIS = [
    "sexe",
    "tournoiTypes3x3.libelle",
    "tournoiType",
]
MEILISEARCH_FACETS_PRATIQUES = [
    "label",
    "type",
]
