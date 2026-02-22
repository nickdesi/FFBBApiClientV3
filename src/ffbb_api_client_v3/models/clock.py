from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Clock:
    minutes: int = 0
    seconds: int = 0
    milliseconds: int = 0

    @staticmethod
    def from_str(obj: str) -> Clock:
        minutes, seconds, milliseconds = obj.split(":") if obj else ["0", "0", "0"]
        return Clock(
            minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds)
        )

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, handler: Any
    ) -> Any:
        from pydantic_core import core_schema

        return core_schema.no_info_before_validator_function(
            cls._parse_pydantic,
            handler(_source_type),
        )

    @classmethod
    def _parse_pydantic(cls, value: Any) -> Any:
        if isinstance(value, str):
            return cls.from_str(value)
        elif isinstance(value, dict):
            return Clock(**value)
        return value

    def to_str(self) -> str:
        return f"{self.minutes}:{self.seconds}:{self.milliseconds}"
