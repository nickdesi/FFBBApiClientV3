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

    def to_str(self) -> str:
        return f"{self.minutes}:{self.seconds}:{self.milliseconds}"
