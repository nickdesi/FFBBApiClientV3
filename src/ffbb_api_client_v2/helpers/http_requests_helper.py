from __future__ import annotations

import json
from collections.abc import Callable
from typing import TypeVar

from requests import ReadTimeout

# Import for backward compatibility - needed by client modules
from ..utils.cache_manager import (  # noqa: F401  # pylint: disable=unused-import
    default_cached_session,
)

T = TypeVar("T")


def catch_result(callback: Callable[[], T], is_retrieving: bool = False) -> T | None:
    """
    Catch the result of a callback function.

    Args:
        callback: The callback function.

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
    except Exception as e:
        raise e
