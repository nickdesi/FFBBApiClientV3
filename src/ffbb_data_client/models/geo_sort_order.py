from enum import Enum


class GeoSortOrder(str, Enum):
    NEAREST_FIRST = "asc"
    FARTHEST_FIRST = "desc"
