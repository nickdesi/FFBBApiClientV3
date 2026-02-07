from __future__ import annotations

from typing import Any, Callable

from .multi_search_result_competitions import CompetitionsMultiSearchResult
from .multi_search_result_organismes import OrganismesMultiSearchResult
from .multi_search_result_pratiques import PratiquesMultiSearchResult
from .multi_search_result_rencontres import RencontresMultiSearchResult
from .multi_search_result_salles import SallesMultiSearchResult
from .multi_search_result_terrains import TerrainsMultiSearchResult
from .multi_search_result_tournois import TournoisMultiSearchResult
from .multi_search_results import MultiSearchResult

index_uids = [
    "ffbbserver_organismes",
    "ffbbserver_rencontres",
    "ffbbserver_terrains",
    "ffbbserver_salles",
    "ffbbserver_tournois",
    "ffbbserver_competitions",
    "ffbbnational_pratiques",
]

index_uids_converters: dict[str, Callable[[Any], MultiSearchResult[Any, Any, Any]]] = {
    index_uids[0]: OrganismesMultiSearchResult.from_dict,
    index_uids[1]: RencontresMultiSearchResult.from_dict,
    index_uids[2]: TerrainsMultiSearchResult.from_dict,
    index_uids[3]: SallesMultiSearchResult.from_dict,
    index_uids[4]: TournoisMultiSearchResult.from_dict,
    index_uids[5]: CompetitionsMultiSearchResult.from_dict,
    index_uids[6]: PratiquesMultiSearchResult.from_dict,
}


def result_from_list(s: list[Any]) -> list[MultiSearchResult[Any, Any, Any]]:
    results: list[MultiSearchResult[Any, Any, Any]] = []

    if s:
        for element in s:
            try:
                index_uid = element["indexUid"]
                from_dict_func = index_uids_converters[index_uid]
                result = from_dict_func(element)
                results.append(result)
            except (KeyError, TypeError, ValueError, AssertionError):
                # Skip invalid or unsupported index results
                pass

    return results


class MultiSearchResults:
    results: list[MultiSearchResult[Any, Any, Any]] | None = None

    def __init__(self, results: list[MultiSearchResult[Any, Any, Any]] | None) -> None:
        self.results = results

    @staticmethod
    def from_dict(obj: Any) -> MultiSearchResults:
        assert isinstance(obj, dict)
        results_raw = obj.get("results")
        results = result_from_list(results_raw) if results_raw is not None else None
        return MultiSearchResults(results)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.results is not None:
            result["results"] = [r.to_dict() for r in self.results]
        return result


def multi_search_results_from_dict(s: Any) -> MultiSearchResults:
    return MultiSearchResults.from_dict(s)
