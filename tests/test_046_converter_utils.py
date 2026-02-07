"""Tests for from_TYPE helper functions in converter_utils."""

from __future__ import annotations

import logging
from datetime import datetime
from enum import Enum
from uuid import UUID

from ffbb_api_client_v2.utils.converter_utils import (
    from_bool,
    from_datetime,
    from_enum,
    from_float,
    from_int,
    from_list,
    from_obj,
    from_str,
    from_uuid,
)

# --- Fixtures / helpers ---


class Color(Enum):
    RED = "red"
    BLUE = "blue"


class SimpleModel:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def from_dict(obj: dict) -> SimpleModel:
        return SimpleModel(obj["name"])


# ==========================================================================
# from_str
# ==========================================================================


class TestFromStr:
    def test_str_returns_str(self):
        assert from_str({"k": "hello"}, "k") == "hello"

    def test_none_returns_none(self):
        assert from_str({"k": None}, "k") is None

    def test_missing_key_returns_none(self):
        assert from_str({}, "k") is None

    def test_int_coerced_to_str(self):
        assert from_str({"k": 42}, "k") == "42"

    def test_float_coerced_to_str(self):
        assert from_str({"k": 3.14}, "k") == "3.14"

    def test_bool_coerced_to_str(self):
        assert from_str({"k": True}, "k") == "True"


# ==========================================================================
# from_int
# ==========================================================================


class TestFromInt:
    def test_int_returns_int(self):
        assert from_int({"k": 42}, "k") == 42

    def test_none_returns_none(self):
        assert from_int({"k": None}, "k") is None

    def test_missing_key_returns_none(self):
        assert from_int({}, "k") is None

    def test_str_coerced_to_int(self):
        assert from_int({"k": "0"}, "k") == 0

    def test_str_negative_coerced(self):
        assert from_int({"k": "-7"}, "k") == -7

    def test_str_non_numeric_warns(self, caplog):
        with caplog.at_level(
            logging.WARNING, logger="ffbb_api_client_v2.utils.converter_utils"
        ):
            result = from_int({"k": "abc"}, "k")
        assert result is None
        assert "cannot parse" in caplog.text

    def test_float_coerced_to_int(self):
        assert from_int({"k": 3.0}, "k") == 3

    def test_bool_not_coerced(self, caplog):
        with caplog.at_level(
            logging.WARNING, logger="ffbb_api_client_v2.utils.converter_utils"
        ):
            result = from_int({"k": True}, "k")
        assert result is None
        assert "unexpected type" in caplog.text


# ==========================================================================
# from_float
# ==========================================================================


class TestFromFloat:
    def test_float_returns_float(self):
        assert from_float({"k": 3.14}, "k") == 3.14

    def test_int_returns_float(self):
        result = from_float({"k": 3}, "k")
        assert result == 3.0
        assert isinstance(result, float)

    def test_none_returns_none(self):
        assert from_float({"k": None}, "k") is None

    def test_missing_key_returns_none(self):
        assert from_float({}, "k") is None

    def test_str_coerced_to_float(self):
        assert from_float({"k": "3.14"}, "k") == 3.14

    def test_str_invalid_warns(self, caplog):
        with caplog.at_level(
            logging.WARNING, logger="ffbb_api_client_v2.utils.converter_utils"
        ):
            result = from_float({"k": "abc"}, "k")
        assert result is None
        assert "cannot parse" in caplog.text

    def test_bool_not_coerced(self, caplog):
        with caplog.at_level(
            logging.WARNING, logger="ffbb_api_client_v2.utils.converter_utils"
        ):
            result = from_float({"k": True}, "k")
        assert result is None
        assert "unexpected type" in caplog.text


# ==========================================================================
# from_bool
# ==========================================================================


class TestFromBool:
    def test_bool_returns_bool(self):
        assert from_bool({"k": True}, "k") is True
        assert from_bool({"k": False}, "k") is False

    def test_none_returns_none(self):
        assert from_bool({"k": None}, "k") is None

    def test_missing_key_returns_none(self):
        assert from_bool({}, "k") is None

    def test_str_true_coerced(self):
        assert from_bool({"k": "true"}, "k") is True

    def test_str_false_coerced(self):
        assert from_bool({"k": "false"}, "k") is False

    def test_str_TRUE_case_insensitive(self):
        assert from_bool({"k": "TRUE"}, "k") is True
        assert from_bool({"k": "False"}, "k") is False

    def test_str_invalid_warns(self, caplog):
        with caplog.at_level(
            logging.WARNING, logger="ffbb_api_client_v2.utils.converter_utils"
        ):
            result = from_bool({"k": "maybe"}, "k")
        assert result is None
        assert "cannot parse" in caplog.text

    def test_int_not_coerced(self, caplog):
        with caplog.at_level(
            logging.WARNING, logger="ffbb_api_client_v2.utils.converter_utils"
        ):
            result = from_bool({"k": 1}, "k")
        assert result is None
        assert "unexpected type" in caplog.text


# ==========================================================================
# from_datetime
# ==========================================================================


class TestFromDatetime:
    def test_iso_string_returns_datetime(self):
        result = from_datetime({"k": "2024-01-01T00:00:00"}, "k")
        assert isinstance(result, datetime)
        assert result.year == 2024

    def test_none_returns_none(self):
        assert from_datetime({"k": None}, "k") is None

    def test_missing_key_returns_none(self):
        assert from_datetime({}, "k") is None

    def test_empty_string_returns_none(self):
        assert from_datetime({"k": ""}, "k") is None

    def test_invalid_string_warns(self, caplog):
        with caplog.at_level(
            logging.WARNING, logger="ffbb_api_client_v2.utils.converter_utils"
        ):
            result = from_datetime({"k": "not-a-date"}, "k")
        assert result is None
        assert "cannot parse" in caplog.text

    def test_non_string_warns(self, caplog):
        with caplog.at_level(
            logging.WARNING, logger="ffbb_api_client_v2.utils.converter_utils"
        ):
            result = from_datetime({"k": 12345}, "k")
        assert result is None
        assert "unexpected type" in caplog.text


# ==========================================================================
# from_enum
# ==========================================================================


class TestFromEnum:
    def test_known_value_returns_member(self):
        assert from_enum(Color, {"k": "red"}, "k") == Color.RED

    def test_none_returns_none(self):
        assert from_enum(Color, {"k": None}, "k") is None

    def test_missing_key_returns_none(self):
        assert from_enum(Color, {}, "k") is None

    def test_unknown_value_warns(self, caplog):
        with caplog.at_level(
            logging.WARNING, logger="ffbb_api_client_v2.utils.converter_utils"
        ):
            result = from_enum(Color, {"k": "unknown"}, "k")
        assert result is None
        assert "unknown value" in caplog.text
        assert "Color" in caplog.text


# ==========================================================================
# from_obj
# ==========================================================================


class TestFromObj:
    def test_dict_calls_from_dict(self):
        result = from_obj(SimpleModel.from_dict, {"k": {"name": "test"}}, "k")
        assert isinstance(result, SimpleModel)
        assert result.name == "test"

    def test_none_returns_none(self):
        assert from_obj(SimpleModel.from_dict, {"k": None}, "k") is None

    def test_missing_key_returns_none(self):
        assert from_obj(SimpleModel.from_dict, {}, "k") is None

    def test_non_dict_warns(self, caplog):
        with caplog.at_level(
            logging.WARNING, logger="ffbb_api_client_v2.utils.converter_utils"
        ):
            result = from_obj(SimpleModel.from_dict, {"k": "string"}, "k")
        assert result is None
        assert "expected dict" in caplog.text


# ==========================================================================
# from_list
# ==========================================================================


class TestFromList:
    def test_list_maps_items(self):
        result = from_list(
            SimpleModel.from_dict,
            {"k": [{"name": "a"}, {"name": "b"}]},
            "k",
        )
        assert len(result) == 2
        assert result[0].name == "a"
        assert result[1].name == "b"

    def test_list_of_primitives(self):
        result = from_list(int, {"k": ["1", "2", "3"]}, "k")
        assert result == [1, 2, 3]

    def test_none_returns_none(self):
        assert from_list(str, {"k": None}, "k") is None

    def test_missing_key_returns_none(self):
        assert from_list(str, {}, "k") is None

    def test_empty_list_returns_empty(self):
        assert from_list(str, {"k": []}, "k") == []

    def test_non_list_warns(self, caplog):
        with caplog.at_level(
            logging.WARNING, logger="ffbb_api_client_v2.utils.converter_utils"
        ):
            result = from_list(str, {"k": "string"}, "k")
        assert result is None
        assert "expected list" in caplog.text


# ==========================================================================
# from_uuid
# ==========================================================================


class TestFromUuid:
    def test_valid_uuid_string(self):
        result = from_uuid({"k": "550e8400-e29b-41d4-a716-446655440000"}, "k")
        assert isinstance(result, UUID)
        assert str(result) == "550e8400-e29b-41d4-a716-446655440000"

    def test_none_returns_none(self):
        assert from_uuid({"k": None}, "k") is None

    def test_missing_key_returns_none(self):
        assert from_uuid({}, "k") is None

    def test_empty_string_returns_none(self):
        assert from_uuid({"k": ""}, "k") is None

    def test_invalid_uuid_warns(self, caplog):
        with caplog.at_level(
            logging.WARNING, logger="ffbb_api_client_v2.utils.converter_utils"
        ):
            result = from_uuid({"k": "not-a-uuid"}, "k")
        assert result is None
        assert "invalid UUID" in caplog.text
