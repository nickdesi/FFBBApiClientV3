from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_list, from_none, from_union
from .multi_search_query import MultiSearchQuery


class MultiSearchQueries:
    queries: list[MultiSearchQuery] | None = None

    def __init__(self, queries: list[MultiSearchQuery] | None = None) -> None:
        self.queries = queries

    @staticmethod
    def from_dict(obj: Any) -> MultiSearchQueries:
        assert isinstance(obj, dict)
        queries = from_union(
            [lambda x: from_list(MultiSearchQuery.from_dict, x), from_none],
            obj.get("queries"),
        )
        return MultiSearchQueries(queries)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.queries is not None:
            result["queries"] = from_union(
                [
                    lambda x: from_list(lambda q: q.to_dict(), x),
                    from_none,
                ],
                self.queries,
            )
        return result


def multi_search_queries_from_dict(s: Any) -> MultiSearchQueries:
    return MultiSearchQueries.from_dict(s)


def multi_search_queries_to_dict(x: MultiSearchQueries) -> Any:
    return x.to_dict()
