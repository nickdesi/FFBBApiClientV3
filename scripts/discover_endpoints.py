#!/usr/bin/env python3
"""
Discover currently exposed FFBB Directus endpoints and searchable Meilisearch indexes.

The script intentionally uses TokenManager so it follows the same token resolution
path as the public client: environment variables first, then the public
configuration endpoint.

Usage:
    python scripts/discover_endpoints.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ffbb_api_client_v3.config import (  # noqa: E402
    API_FFBB_BASE_URL,
    DEFAULT_USER_AGENT,
    ENDPOINT_OPENAPI,
    MEILISEARCH_BASE_URL,
    MEILISEARCH_ENDPOINT_MULTI_SEARCH,
    MEILISEARCH_INDEX_COMPETITIONS,
    MEILISEARCH_INDEX_ENGAGEMENTS,
    MEILISEARCH_INDEX_FORMATIONS,
    MEILISEARCH_INDEX_GALERIES,
    MEILISEARCH_INDEX_NEWS,
    MEILISEARCH_INDEX_ORGANISMES,
    MEILISEARCH_INDEX_PRATIQUES,
    MEILISEARCH_INDEX_RENCONTRES,
    MEILISEARCH_INDEX_RSS,
    MEILISEARCH_INDEX_SALLES,
    MEILISEARCH_INDEX_TERRAINS,
    MEILISEARCH_INDEX_TOURNOIS,
    MEILISEARCH_INDEX_YOUTUBE_VIDEOS,
)
from ffbb_api_client_v3.helpers.http_requests_utils import (  # noqa: E402
    http_get_json,
    http_post_json,
)
from ffbb_api_client_v3.utils.token_manager import TokenManager  # noqa: E402

DATA_DIR = PROJECT_ROOT / "data"
REPORT_PATH = DATA_DIR / "endpoint_discovery.json"

MEILI_CANDIDATE_INDEXES = [
    MEILISEARCH_INDEX_ORGANISMES,
    MEILISEARCH_INDEX_RENCONTRES,
    MEILISEARCH_INDEX_TERRAINS,
    MEILISEARCH_INDEX_SALLES,
    MEILISEARCH_INDEX_TOURNOIS,
    MEILISEARCH_INDEX_COMPETITIONS,
    MEILISEARCH_INDEX_ENGAGEMENTS,
    MEILISEARCH_INDEX_FORMATIONS,
    MEILISEARCH_INDEX_PRATIQUES,
    MEILISEARCH_INDEX_NEWS,
    MEILISEARCH_INDEX_YOUTUBE_VIDEOS,
    MEILISEARCH_INDEX_RSS,
    MEILISEARCH_INDEX_GALERIES,
    "ffbbserver_sessions",
    "genius_sport_matches",
    "genius_sports_live_logs",
    "rematch_videos",
    "edf_matches",
    "edf_players",
    "edf_teams",
]


def _extract_item_collections(openapi: dict[str, Any]) -> list[str]:
    collections: set[str] = set()
    for path in openapi.get("paths", {}):
        if not path.startswith("/items/"):
            continue
        collection = path.removeprefix("/items/").removesuffix("/{id}")
        collections.add(collection)
    return sorted(collections)


def _probe_meili_indexes(token: str) -> list[dict[str, Any]]:
    url = f"{MEILISEARCH_BASE_URL}{MEILISEARCH_ENDPOINT_MULTI_SEARCH}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "user-agent": DEFAULT_USER_AGENT,
    }
    discovered: list[dict[str, Any]] = []

    for index_uid in MEILI_CANDIDATE_INDEXES:
        payload = {"queries": [{"indexUid": index_uid, "q": "", "limit": 1}]}
        try:
            response = http_post_json(url, headers, data=payload, timeout=30)
        except Exception as exc:
            discovered.append(
                {"indexUid": index_uid, "available": False, "error": str(exc)}
            )
            continue

        results = response.get("results", []) if isinstance(response, dict) else []
        result = results[0] if results else {}
        discovered.append(
            {
                "indexUid": index_uid,
                "available": bool(results),
                "estimatedTotalHits": result.get("estimatedTotalHits"),
                "sampleKeys": (
                    sorted(result.get("hits", [{}])[0].keys())
                    if result.get("hits")
                    else []
                ),
            }
        )

    return discovered


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tokens = TokenManager.get_tokens()

    api_headers = {
        "Authorization": f"Bearer {tokens.api_token}",
        "user-agent": DEFAULT_USER_AGENT,
    }
    openapi = http_get_json(
        f"{API_FFBB_BASE_URL}{ENDPOINT_OPENAPI}",
        api_headers,
        timeout=60,
    )

    collections = _extract_item_collections(openapi)
    meili_indexes = _probe_meili_indexes(tokens.meilisearch_token)

    report = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "api_base_url": API_FFBB_BASE_URL,
            "meilisearch_base_url": MEILISEARCH_BASE_URL,
            "openapi_version": openapi.get("info", {}).get("version"),
        },
        "directus": {
            "collections": collections,
            "item_paths": [f"items/{collection}" for collection in collections],
        },
        "meilisearch": {
            "indexes": meili_indexes,
            "available_indexes": [
                item["indexUid"] for item in meili_indexes if item["available"]
            ],
        },
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)

    print(f"Directus collections: {len(collections)}")
    print(
        f"Available Meilisearch indexes: {len(report['meilisearch']['available_indexes'])}"
    )
    print(f"Report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
