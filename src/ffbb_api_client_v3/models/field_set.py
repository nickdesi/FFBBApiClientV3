from enum import Enum


class FieldSet(Enum):
    """Enum for different field sets.

    Since v1.4.0, BASIC and DETAILED are aliases for DEFAULT.
    All queries use the comprehensive DEFAULT field list.
    """

    BASIC = "default"
    DEFAULT = "default"
    DETAILED = "default"
    MINIMAL = "minimal"
