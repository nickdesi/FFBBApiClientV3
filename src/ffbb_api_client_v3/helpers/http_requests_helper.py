"""HTTP request helper utilities for FFBB API Client."""

from __future__ import annotations

import json
from collections.abc import Callable, Coroutine
from typing import Any, TypeVar

from httpx import ReadTimeout

__all__ = ["async_catch_result", "catch_result"]

T = TypeVar("T")


def catch_result(callback: Callable[[], T], is_retrieving: bool = False) -> T | None:
    """
    Catch the result of a callback function.

    Args:
        callback: The callback function.
        is_retrieving: Whether this is a retry attempt.

    Returns:
        The result of the callback function or None if an exception occurs.
    """

    try:
        return callback()
    except json.decoder.JSONDecodeError as e:
        if e.msg == "Expecting value":
            return None
        raise e
    except ReadTimeout as e:
        if not is_retrieving:
            return catch_result(callback, True)
        raise e
    except ConnectionError as e:
        if not is_retrieving:
            return catch_result(callback, True)
        raise e


async def async_catch_result(
    coro: Coroutine[Any, Any, T], is_retrieving: bool = False
) -> T | None:
    """
    Catch the result of an awaitable coroutine.

    Mirrors the behaviour of :func:`catch_result` for async call sites:
    retries once on transient network errors, returns ``None`` on empty JSON.

    Args:
        coro: The coroutine to await.
        is_retrieving: Whether this is a retry attempt.

    Returns:
        The result of the coroutine or None if a recoverable exception occurs.
    """
    try:
        return await coro
    except json.decoder.JSONDecodeError as e:
        if e.msg == "Expecting value":
            return None
        raise
    except ReadTimeout as e:
        if not is_retrieving:
            return None  # caller already has retry logic via retry_utils
        raise e
    except ConnectionError as e:
        if not is_retrieving:
            return None
        raise e
