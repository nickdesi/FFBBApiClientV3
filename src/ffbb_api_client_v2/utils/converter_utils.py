from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import datetime
from enum import Enum
from typing import Any, TypeVar
from uuid import UUID

import dateutil.parser

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)

logger = logging.getLogger(__name__)


def from_officiels_list(x: Any) -> list | None:
    """
    Handle officiels field which can be either:
    - A comma-separated string (old format)
    - A list of dicts (new format)
    - None
    """
    if x is None:
        return None
    if isinstance(x, list):
        return x  # Return as-is if already a list
    if isinstance(x, str):
        return [s.strip() for s in x.split(",")] if x else None
    return None


# ---------------------------------------------------------------------------
# from_TYPE helpers — direct dict-key extraction with type coercion
# ---------------------------------------------------------------------------


def from_str(obj: dict, key: str) -> str | None:
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, str):
        return x
    try:
        return str(x)
    except (TypeError, ValueError):
        logger.warning(
            "from_str(%r): cannot convert %s to str (value: %.100r)",
            key,
            type(x).__name__,
            x,
        )
        return None


def from_int(obj: dict, key: str) -> int | None:
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, int) and not isinstance(x, bool):
        return x
    if isinstance(x, str):
        try:
            return int(x)
        except ValueError:
            logger.warning("from_int(%r): cannot parse %r as int", key, x)
            return None
    if isinstance(x, float):
        return int(x)
    logger.warning(
        "from_int(%r): unexpected type %s (value: %.100r)",
        key,
        type(x).__name__,
        x,
    )
    return None


def from_float(obj: dict, key: str) -> float | None:
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, (float, int)) and not isinstance(x, bool):
        return float(x)
    if isinstance(x, str):
        try:
            return float(x)
        except ValueError:
            logger.warning("from_float(%r): cannot parse %r as float", key, x)
            return None
    logger.warning(
        "from_float(%r): unexpected type %s (value: %.100r)",
        key,
        type(x).__name__,
        x,
    )
    return None


def from_bool(obj: dict, key: str) -> bool | None:
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, bool):
        return x
    if isinstance(x, str):
        if x.lower() == "true":
            return True
        if x.lower() == "false":
            return False
        logger.warning("from_bool(%r): cannot parse %r as bool", key, x)
        return None
    logger.warning(
        "from_bool(%r): unexpected type %s (value: %.100r)",
        key,
        type(x).__name__,
        x,
    )
    return None


def from_datetime(obj: dict, key: str) -> datetime | None:
    x = obj.get(key)
    if not x:
        return None
    if isinstance(x, str):
        try:
            result: datetime = dateutil.parser.parse(x)
            return result
        except (ValueError, dateutil.parser.ParserError):
            logger.warning("from_datetime(%r): cannot parse %r as datetime", key, x)
            return None
    logger.warning(
        "from_datetime(%r): unexpected type %s (value: %.100r)",
        key,
        type(x).__name__,
        x,
    )
    return None


def from_enum(enum_class: type[EnumT], obj: dict, key: str) -> EnumT | None:
    x = obj.get(key)
    if x is None:
        return None
    try:
        return enum_class(x)
    except ValueError:
        logger.warning(
            "from_enum(%s, %r): unknown value %r",
            enum_class.__name__,
            key,
            x,
        )
        return None


def from_obj(from_dict_fn: Callable[[Any], T], obj: dict, key: str) -> T | None:
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, dict):
        return from_dict_fn(x)
    logger.warning(
        "from_obj(%r): expected dict or None, got %s",
        key,
        type(x).__name__,
    )
    return None


def from_list(item_fn: Callable[[Any], T], obj: dict, key: str) -> list[T] | None:
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, list):
        return [item_fn(item) for item in x]
    logger.warning(
        "from_list(%r): expected list or None, got %s",
        key,
        type(x).__name__,
    )
    return None


def from_uuid(obj: dict, key: str) -> UUID | None:
    x = obj.get(key)
    if not x:
        return None
    try:
        return UUID(x) if isinstance(x, str) else None
    except ValueError:
        logger.warning("from_uuid(%r): invalid UUID %r", key, x)
        return None
