"""Token management for FFBB API clients."""

from __future__ import annotations

import os
from dataclasses import dataclass

from ..config import (
    API_FFBB_BASE_URL,
    DEFAULT_USER_AGENT,
    ENDPOINT_CONFIGURATION,
    ENV_API_TOKEN,
    ENV_MEILISEARCH_TOKEN,
)
from ..helpers.http_requests_helper import catch_result
from ..helpers.http_requests_utils import http_get_json
from ..models.configuration_models import GetConfigurationResponse
from ..utils.cache_manager import CacheConfig, get_cache_manager


@dataclass
class FFBBTokens:
    """Container for FFBB API tokens."""

    api_token: str
    meilisearch_token: str


class TokenManager:
    """
    Manages FFBB API tokens.

    Resolution order:
    1. Environment variables
    2. Fetch from FFBB API configuration endpoint (public, HTTP cached)

    Example:
        tokens = TokenManager.get_tokens()
        client = FFBBAPIClientV2.create(
            api_bearer_token=tokens.api_token,
            meilisearch_bearer_token=tokens.meilisearch_token
        )
    """

    @staticmethod
    def get_tokens(cache_config: CacheConfig | None = None) -> FFBBTokens:
        """
        Get FFBB tokens from environment or API.

        Args:
            cache_config: Optional cache configuration for HTTP requests.
                If None, uses the default cache manager.

        Returns:
            FFBBTokens with api_token and meilisearch_token
        """
        # Try environment variables first
        api_token = os.getenv(ENV_API_TOKEN)
        meilisearch_token = os.getenv(ENV_MEILISEARCH_TOKEN)

        if api_token and meilisearch_token:
            return FFBBTokens(api_token=api_token, meilisearch_token=meilisearch_token)

        # Fetch from API (HTTP layer handles caching)
        config = TokenManager._fetch_configuration(cache_config)
        return FFBBTokens(
            api_token=config.api_bearer_token,
            meilisearch_token=config.meilisearch_token,
        )

    @staticmethod
    def _fetch_configuration(
        cache_config: CacheConfig | None = None,
    ) -> GetConfigurationResponse:
        """Fetch configuration from FFBB API (public endpoint)."""
        cache_manager = get_cache_manager(cache_config)
        cached_session = cache_manager.get_session()

        config_url = f"{API_FFBB_BASE_URL}{ENDPOINT_CONFIGURATION}"
        headers = {"user-agent": DEFAULT_USER_AGENT}

        data = catch_result(
            lambda: http_get_json(
                config_url,
                headers,
                cached_session=cached_session,
            )
        )

        actual_data = data.get("data") if data and isinstance(data, dict) else data

        if not actual_data:
            raise RuntimeError("Failed to fetch configuration from FFBB API")

        return GetConfigurationResponse.from_dict(actual_data)
