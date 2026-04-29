"""Extension methods for ApiFFBBAppClient — new REST endpoints.

These methods implement access to REST collections not yet covered by the
main client::

    ffbbserver_rencontres
    ffbbserver_officiels
    ffbbserver_entraineurs

Usage example::

    from ffbb_api_client_v3.clients.api_ffbb_app_client_extensions import (
        get_rencontre,
        get_officiel,
        get_entraineur,
    )
    rencontre = get_rencontre(client, 12345)
    officiel = get_officiel(client, 67890)

TODO: these methods should be merged directly into ApiFFBBAppClient
once validated.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import httpx
from httpx import Client
from pydantic import TypeAdapter

if TYPE_CHECKING:
    from .api_ffbb_app_client import ApiFFBBAppClient

from ..config import (
    ENDPOINT_ENTRAINEURS,
    ENDPOINT_OFFICIELS,
    ENDPOINT_RENCONTRES,
    ENDPOINT_ASSETS,
)
from ..helpers.http_requests_helper import catch_result
from ..helpers.http_requests_utils import (
    http_get_json,
    http_get_json_async,
    url_with_params,
)
from ..models.get_rencontre_response import GetRencontreResponse
from ..models.get_officiel_response import GetOfficielResponse
from ..models.get_entraineur_response import GetEntraineurResponse


def get_rencontre(
    client: "ApiFFBBAppClient",
    rencontre_id: int,
    fields: list[str] | None = None,
    cached_session: Client | None = None,
) -> GetRencontreResponse | None:
    """Retrieve a single rencontre by its Directus ID.

    Args:
        client: The ApiFFBBAppClient instance.
        rencontre_id: The integer ID of the rencontre.
        fields: Optional list of Directus fields to fetch.
        cached_session: Optional HTTP cache session.

    Returns:
        GetRencontreResponse or None if not found.
    """
    url = f"{client.url}{ENDPOINT_RENCONTRES}/{rencontre_id}"
    params: dict[str, Any] = {}
    if fields:
        params["fields[]"] = fields

    final_url = url_with_params(url, params) if params else url
    data = catch_result(
        lambda: http_get_json(
            final_url,
            client.headers,
            debug=client.debug,
            cached_session=cached_session or client.cached_session,
            retry_config=client.retry_config,
            timeout_config=client.timeout_config,
        )
    )
    actual_data = data.get("data") if data and isinstance(data, dict) else data
    if actual_data:
        return GetRencontreResponse.from_dict(actual_data)
    return None


async def get_rencontre_async(
    client: "ApiFFBBAppClient",
    rencontre_id: int,
    fields: list[str] | None = None,
    cached_session: httpx.AsyncClient | None = None,
) -> GetRencontreResponse | None:
    """Retrieve a single rencontre by its Directus ID asynchronously."""
    url = f"{client.url}{ENDPOINT_RENCONTRES}/{rencontre_id}"
    params: dict[str, Any] = {}
    if fields:
        params["fields[]"] = fields

    final_url = url_with_params(url, params) if params else url
    try:
        data = await http_get_json_async(
            final_url,
            client.headers,
            debug=client.debug,
            cached_session=cached_session or client.async_cached_session,
            retry_config=client.retry_config,
            timeout_config=client.timeout_config,
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data:
            return GetRencontreResponse.from_dict(actual_data)
    except Exception as e:
        if client.debug:
            client.logger.error(f"Error in get_rencontre_async: {e}")
    return None


def get_officiel(
    client: "ApiFFBBAppClient",
    officiel_id: int,
    fields: list[str] | None = None,
    cached_session: Client | None = None,
) -> GetOfficielResponse | None:
    """Retrieve a single officiel (arbitre) by its Directus ID.

    Args:
        client: The ApiFFBBAppClient instance.
        officiel_id: The integer ID of the officiel.
        fields: Optional list of Directus fields to fetch.
        cached_session: Optional HTTP cache session.

    Returns:
        GetOfficielResponse or None if not found.
    """
    url = f"{client.url}{ENDPOINT_OFFICIELS}/{officiel_id}"
    params: dict[str, Any] = {}
    if fields:
        params["fields[]"] = fields

    final_url = url_with_params(url, params) if params else url
    data = catch_result(
        lambda: http_get_json(
            final_url,
            client.headers,
            debug=client.debug,
            cached_session=cached_session or client.cached_session,
            retry_config=client.retry_config,
            timeout_config=client.timeout_config,
        )
    )
    actual_data = data.get("data") if data and isinstance(data, dict) else data
    if actual_data:
        return GetOfficielResponse.from_dict(actual_data)
    return None


async def get_officiel_async(
    client: "ApiFFBBAppClient",
    officiel_id: int,
    fields: list[str] | None = None,
    cached_session: httpx.AsyncClient | None = None,
) -> GetOfficielResponse | None:
    """Retrieve a single officiel asynchronously."""
    url = f"{client.url}{ENDPOINT_OFFICIELS}/{officiel_id}"
    params: dict[str, Any] = {}
    if fields:
        params["fields[]"] = fields

    final_url = url_with_params(url, params) if params else url
    try:
        data = await http_get_json_async(
            final_url,
            client.headers,
            debug=client.debug,
            cached_session=cached_session or client.async_cached_session,
            retry_config=client.retry_config,
            timeout_config=client.timeout_config,
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data:
            return GetOfficielResponse.from_dict(actual_data)
    except Exception as e:
        if client.debug:
            client.logger.error(f"Error in get_officiel_async: {e}")
    return None


def get_entraineur(
    client: "ApiFFBBAppClient",
    entraineur_id: int,
    fields: list[str] | None = None,
    cached_session: Client | None = None,
) -> GetEntraineurResponse | None:
    """Retrieve a single entraîner by its Directus ID.

    Args:
        client: The ApiFFBBAppClient instance.
        entraineur_id: The integer ID of the entraîner.
        fields: Optional list of Directus fields to fetch.
        cached_session: Optional HTTP cache session.

    Returns:
        GetEntraineurResponse or None if not found.
    """
    url = f"{client.url}{ENDPOINT_ENTRAINEURS}/{entraineur_id}"
    params: dict[str, Any] = {}
    if fields:
        params["fields[]"] = fields

    final_url = url_with_params(url, params) if params else url
    data = catch_result(
        lambda: http_get_json(
            final_url,
            client.headers,
            debug=client.debug,
            cached_session=cached_session or client.cached_session,
            retry_config=client.retry_config,
            timeout_config=client.timeout_config,
        )
    )
    actual_data = data.get("data") if data and isinstance(data, dict) else data
    if actual_data:
        return GetEntraineurResponse.from_dict(actual_data)
    return None


async def get_entraineur_async(
    client: "ApiFFBBAppClient",
    entraineur_id: int,
    fields: list[str] | None = None,
    cached_session: httpx.AsyncClient | None = None,
) -> GetEntraineurResponse | None:
    """Retrieve a single entraîner asynchronously."""
    url = f"{client.url}{ENDPOINT_ENTRAINEURS}/{entraineur_id}"
    params: dict[str, Any] = {}
    if fields:
        params["fields[]"] = fields

    final_url = url_with_params(url, params) if params else url
    try:
        data = await http_get_json_async(
            final_url,
            client.headers,
            debug=client.debug,
            cached_session=cached_session or client.async_cached_session,
            retry_config=client.retry_config,
            timeout_config=client.timeout_config,
        )
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data:
            return GetEntraineurResponse.from_dict(actual_data)
    except Exception as e:
        if client.debug:
            client.logger.error(f"Error in get_entraineur_async: {e}")
    return None


def get_asset_url(
    client: "ApiFFBBAppClient",
    asset_uuid: str,
    width: int | None = None,
    height: int | None = None,
    format: str | None = None,
    quality: int | None = None,
) -> str:
    """Build a Directus asset URL for a given file UUID.

    Args:
        client: The ApiFFBBAppClient instance.
        asset_uuid: The UUID of the file/image asset.
        width: Optional image width in pixels.
        height: Optional image height in pixels.
        format: Optional image format (e.g. 'webp', 'jpg', 'png').
        quality: Optional image quality (1-100).

    Returns:
        A fully-formed asset URL string.
    """
    url = f"{client.url}{ENDPOINT_ASSETS}/{asset_uuid}"
    params: dict[str, Any] = {}
    if width is not None:
        params["width"] = str(width)
    if height is not None:
        params["height"] = str(height)
    if format is not None:
        params["format"] = format
    if quality is not None:
        params["quality"] = str(quality)

    return url_with_params(url, params) if params else url
