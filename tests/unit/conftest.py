"""Unit test configuration - inherits from parent conftest.py."""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest


@pytest.fixture
def mock_httpx_response() -> MagicMock:
    """Return a pre-configured mock httpx.Response with JSON support.

    Usage::

        def test_something(mock_httpx_response):
            mock_httpx_response.json.return_value = {"key": "value"}
    """
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = 200
    resp.text = "{}"
    resp.json.return_value = {}
    resp.raise_for_status = MagicMock()
    return resp


@pytest.fixture
def make_mock_response():
    """Factory fixture for mock httpx.Response with custom payload.

    Usage::

        def test_something(make_mock_response):
            resp = make_mock_response({"results": []}, status_code=200)
    """

    def _factory(payload: Any = None, status_code: int = 200) -> MagicMock:
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = status_code
        body = json.dumps(payload) if payload is not None else "{}"
        resp.text = body
        resp.json.return_value = payload or {}
        resp.raise_for_status = MagicMock()
        if status_code >= 400:
            resp.raise_for_status.side_effect = httpx.HTTPStatusError(
                f"HTTP {status_code}",
                request=MagicMock(spec=httpx.Request),
                response=resp,
            )
        return resp

    return _factory


@pytest.fixture
def mock_httpx_client(mock_httpx_response: MagicMock) -> MagicMock:
    """Sync httpx.Client mock with .get() and .post() pre-configured.

    Usage::

        def test_something(mock_httpx_client):
            mock_httpx_client.get.return_value.text = '{"ok": true}'
    """
    client = MagicMock(spec=httpx.Client)
    client.get.return_value = mock_httpx_response
    client.post.return_value = mock_httpx_response
    return client


@pytest.fixture
def mock_httpx_async_client(mock_httpx_response: MagicMock) -> AsyncMock:
    """Async httpx.AsyncClient mock with awaitable .get() and .post().

    Usage::

        async def test_something(mock_httpx_async_client):
            mock_httpx_async_client.get.return_value.text = '{"ok": true}'
    """
    client = AsyncMock(spec=httpx.AsyncClient)
    client.get.return_value = mock_httpx_response
    client.post.return_value = mock_httpx_response
    return client
