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
