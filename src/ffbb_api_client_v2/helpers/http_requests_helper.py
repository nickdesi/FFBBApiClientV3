"""HTTP request helper utilities for FFBB API Client."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import TypeVar

from requests import ReadTimeout

__all__ = ["catch_result"]

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
