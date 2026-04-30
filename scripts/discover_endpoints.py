#!/usr/bin/env python3
"""
Discover the latest exposed FFBB Directus endpoints and searchable Meilisearch indexes.

The script intentionally uses TokenManager so it follows the same token resolution
path as the public client: environment variables first, then the public
configuration endpoint.

It refreshes versioned discovery artefacts under ``data/`` and writes a compact
change summary suitable for CI/GitHub Actions.

Usage:
    python scripts/discover_endpoints.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
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
from ffbb_api_client_v3.utils.cache_manager import CacheConfig  # noqa: E402
from ffbb_api_client_v3.utils.token_manager import TokenManager  # noqa: E402

DATA_DIR = PROJECT_ROOT / "data"
REPORT_PATH = DATA_DIR / "endpoint_discovery.json"
COLLECTIONS_PATH = DATA_DIR / "collections.json"
INDEXES_PATH = DATA_DIR / "indexes.json"
OPENAPI_PATH = DATA_DIR / "openapi.json"
OPENAPI_FULL_PATH = DATA_DIR / "openapi_full.json"
CHANGE_SUMMARY_PATH = DATA_DIR / "api_update_summary.md"

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


def _load_json(path: Path) -> Any | None:
    if not path.exists():
        return None
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError:
        return None


def _write_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write("\n")


def _strip_volatile_metadata(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {
            key: _strip_volatile_metadata(value)
            for key, value in payload.items()
            if not (key == "timestamp" and "source" in payload)
            and not (key == "timestamp" and "api_base_url" in payload)
        }
    if isinstance(payload, list):
        return [_strip_volatile_metadata(item) for item in payload]
    return payload


def _write_json_if_changed(path: Path, payload: Any) -> bool:
    previous = _load_json(path)
    if _strip_volatile_metadata(previous) == _strip_volatile_metadata(payload):
        return False
    _write_json(path, payload)
    return True


def _stable_hash(payload: Any) -> str:
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _extract_item_collections(openapi: dict[str, Any]) -> list[str]:
    collections: set[str] = set()
    for path in openapi.get("paths", {}):
        if not path.startswith("/items/"):
            continue
        collection = path.removeprefix("/items/").removesuffix("/{id}")
        collections.add(collection)
    return sorted(collections)


def _extract_item_paths(openapi: dict[str, Any]) -> dict[str, list[str]]:
    item_paths: dict[str, list[str]] = {}
    for path, operations in openapi.get("paths", {}).items():
        if not path.startswith("/items/") or not isinstance(operations, dict):
            continue
        item_paths[path.removeprefix("/")] = sorted(operations)
    return dict(sorted(item_paths.items()))


def _build_openapi_snapshot(openapi: dict[str, Any]) -> dict[str, Any]:
    """Build a compact, stable OpenAPI snapshot for reviewing API drift."""
    schemas = openapi.get("components", {}).get("schemas", {})
    return {
        "openapi": openapi.get("openapi"),
        "info": openapi.get("info", {}),
        "servers": openapi.get("servers", []),
        "paths": {
            path: operations
            for path, operations in sorted(openapi.get("paths", {}).items())
            if path.startswith(("/items/", "/assets", "/files"))
        },
        "components": {
            "schemas": {
                key: schemas[key]
                for key in sorted(schemas)
                if key.startswith(("Items", "Files"))
            }
        },
    }


def _probe_meili_indexes(token: str) -> list[dict[str, Any]]:
    url = f"{MEILISEARCH_BASE_URL}{MEILISEARCH_ENDPOINT_MULTI_SEARCH}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "user-agent": DEFAULT_USER_AGENT,
    }
    discovered: list[dict[str, Any]] = []

    for index_uid in sorted(set(MEILI_CANDIDATE_INDEXES)):
        payload = {"queries": [{"indexUid": index_uid, "q": "", "limit": 1}]}
        try:
            response = http_post_json(url, headers, data=payload, timeout=30)
        except Exception:
            discovered.append(
                {
                    "indexUid": index_uid,
                    "available": False,
                    "status": "not_available",
                }
            )
            continue

        results = response.get("results", []) if isinstance(response, dict) else []
        result = results[0] if results else {}
        discovered.append(
            {
                "indexUid": index_uid,
                "available": bool(results),
                "status": "available" if results else "empty_or_not_available",
                "estimatedTotalHits": result.get("estimatedTotalHits"),
                "sampleKeys": (
                    sorted(result.get("hits", [{}])[0].keys())
                    if result.get("hits")
                    else []
                ),
            }
        )

    return discovered


def _diff_lists(before: list[str], after: list[str]) -> dict[str, list[str]]:
    before_set = set(before)
    after_set = set(after)
    return {
        "added": sorted(after_set - before_set),
        "removed": sorted(before_set - after_set),
        "unchanged": sorted(before_set & after_set),
    }


def _previous_collections(previous: Any) -> list[str]:
    if isinstance(previous, dict):
        if isinstance(previous.get("collections"), list):
            return previous["collections"]
        if isinstance(previous.get("directus"), dict):
            collections = previous["directus"].get("collections")
            if isinstance(collections, list):
                return collections
    if isinstance(previous, list):
        return previous
    return []


def _previous_indexes(previous: Any) -> list[str]:
    if isinstance(previous, dict):
        if isinstance(previous.get("available_indexes"), list):
            return previous["available_indexes"]
        if isinstance(previous.get("meilisearch"), dict):
            indexes = previous["meilisearch"].get("available_indexes")
            if isinstance(indexes, list):
                return indexes
    if isinstance(previous, list):
        return previous
    return []


def _build_change_summary(
    *,
    previous_report: Any,
    previous_collections: Any,
    previous_indexes: Any,
    previous_openapi_snapshot: Any,
    report: dict[str, Any],
    collections_payload: dict[str, Any],
    indexes_payload: dict[str, Any],
    openapi_snapshot: dict[str, Any],
) -> str:
    collections_diff = _diff_lists(
        _previous_collections(previous_collections or previous_report),
        collections_payload["collections"],
    )
    indexes_diff = _diff_lists(
        _previous_indexes(previous_indexes or previous_report),
        indexes_payload["available_indexes"],
    )

    previous_paths = (
        sorted(previous_openapi_snapshot.get("paths", {}))
        if isinstance(previous_openapi_snapshot, dict)
        else []
    )
    current_paths = sorted(openapi_snapshot.get("paths", {}))
    paths_diff = _diff_lists(previous_paths, current_paths)

    lines = [
        "# FFBB API update summary",
        "",
        f"- Timestamp: `{report['metadata']['timestamp']}`",
        f"- API base URL: `{report['metadata']['api_base_url']}`",
        f"- Meilisearch base URL: `{report['metadata']['meilisearch_base_url']}`",
        f"- OpenAPI version: `{report['metadata']['openapi_version']}`",
        f"- OpenAPI SHA256: `{report['metadata']['openapi_sha256']}`",
        "",
        "## Directus collections",
        f"- Total: `{len(collections_payload['collections'])}`",
        f"- Added: {collections_diff['added'] or 'None'}",
        f"- Removed: {collections_diff['removed'] or 'None'}",
        "",
        "## Directus item paths",
        f"- Total: `{len(current_paths)}`",
        f"- Added: {paths_diff['added'] or 'None'}",
        f"- Removed: {paths_diff['removed'] or 'None'}",
        "",
        "## Meilisearch indexes",
        f"- Available total: `{len(indexes_payload['available_indexes'])}`",
        f"- Added: {indexes_diff['added'] or 'None'}",
        f"- Removed: {indexes_diff['removed'] or 'None'}",
        "",
        "Generated by `python scripts/discover_endpoints.py`.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    previous_report = _load_json(REPORT_PATH)
    previous_collections = _load_json(COLLECTIONS_PATH)
    previous_indexes = _load_json(INDEXES_PATH)
    previous_openapi_snapshot = _load_json(OPENAPI_PATH)

    tokens = TokenManager.get_tokens(cache_config=CacheConfig(enabled=False))

    api_headers = {
        "Authorization": f"Bearer {tokens.api_token}",
        "user-agent": DEFAULT_USER_AGENT,
    }
    openapi = http_get_json(
        f"{API_FFBB_BASE_URL}{ENDPOINT_OPENAPI}",
        api_headers,
        timeout=60,
    )

    timestamp = datetime.now(timezone.utc).isoformat()
    collections = _extract_item_collections(openapi)
    item_paths = _extract_item_paths(openapi)
    meili_indexes = _probe_meili_indexes(tokens.meilisearch_token)
    available_indexes = [
        item["indexUid"] for item in meili_indexes if item["available"]
    ]
    openapi_snapshot = _build_openapi_snapshot(openapi)

    collections_payload = {
        "metadata": {
            "timestamp": timestamp,
            "source": f"{API_FFBB_BASE_URL}{ENDPOINT_OPENAPI}",
            "openapi_version": openapi.get("info", {}).get("version"),
        },
        "collections": collections,
        "item_paths": [f"items/{collection}" for collection in collections],
        "paths": item_paths,
    }
    indexes_payload = {
        "metadata": {
            "timestamp": timestamp,
            "source": f"{MEILISEARCH_BASE_URL}{MEILISEARCH_ENDPOINT_MULTI_SEARCH}",
        },
        "available_indexes": available_indexes,
        "indexes": [item for item in meili_indexes if item["available"]],
        "unavailable_indexes": [
            {
                "indexUid": item["indexUid"],
                "status": item.get("status", "not_available"),
            }
            for item in meili_indexes
            if not item["available"]
        ],
    }
    report = {
        "metadata": {
            "timestamp": timestamp,
            "api_base_url": API_FFBB_BASE_URL,
            "meilisearch_base_url": MEILISEARCH_BASE_URL,
            "openapi_version": openapi.get("info", {}).get("version"),
            "openapi_sha256": _stable_hash(openapi),
            "openapi_snapshot_sha256": _stable_hash(openapi_snapshot),
        },
        "directus": collections_payload,
        "meilisearch": indexes_payload,
    }

    summary = _build_change_summary(
        previous_report=previous_report,
        previous_collections=previous_collections,
        previous_indexes=previous_indexes,
        previous_openapi_snapshot=previous_openapi_snapshot,
        report=report,
        collections_payload=collections_payload,
        indexes_payload=indexes_payload,
        openapi_snapshot=openapi_snapshot,
    )

    changed = [
        _write_json_if_changed(OPENAPI_FULL_PATH, openapi),
        _write_json_if_changed(OPENAPI_PATH, openapi_snapshot),
        _write_json_if_changed(COLLECTIONS_PATH, collections_payload),
        _write_json_if_changed(INDEXES_PATH, indexes_payload),
        _write_json_if_changed(REPORT_PATH, report),
    ]
    if any(changed) or not CHANGE_SUMMARY_PATH.exists():
        CHANGE_SUMMARY_PATH.write_text(summary, encoding="utf-8")

    print(f"Directus collections: {len(collections)}")
    print(f"Directus item paths: {len(item_paths)}")
    print(f"Available Meilisearch indexes: {len(available_indexes)}")
    print(f"OpenAPI SHA256: {report['metadata']['openapi_sha256']}")
    print(f"Report written to: {REPORT_PATH}")
    print(f"Change summary written to: {CHANGE_SUMMARY_PATH}")


if __name__ == "__main__":
    main()
