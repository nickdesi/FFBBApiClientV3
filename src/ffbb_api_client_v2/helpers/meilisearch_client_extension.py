from __future__ import annotations

from collections.abc import Sequence

from requests_cache import CachedSession

from ..clients.meilisearch_client import MeilisearchClient
from ..models.multi_search_query import MultiSearchQuery
from ..models.multi_search_results_class import MultiSearchResults
from .http_requests_helper import default_cached_session


class MeilisearchClientExtension(MeilisearchClient):
    def __init__(
        self,
        bearer_token: str,
        url: str,
        debug: bool = False,
        cached_session: CachedSession | None = default_cached_session,
    ):
        super().__init__(bearer_token, url, debug, cached_session)

    def smart_multi_search(
        self,
        queries: Sequence[MultiSearchQuery] | None = None,
        cached_session: CachedSession | None = None,
    ) -> MultiSearchResults | None:
        results = self.multi_search(queries, cached_session)

        # Should filter results.hits according to query.q
        if queries and results and results.results:
            for i in range(len(results.results)):
                query = queries[i]

                if query.q:
                    result = results.results[i]
                    results.results[i] = query.filter_result(result)

        return results

    def recursive_smart_multi_search(
        self,
        queries: Sequence[MultiSearchQuery] | None = None,
        cached_session: CachedSession | None = None,
    ) -> MultiSearchResults | None:
        result = self.smart_multi_search(queries, cached_session)
        if not result or not queries or not result.results:
            return result

        next_queries: list[MultiSearchQuery] = []

        for i in range(len(result.results)):
            query_result = result.results[i]
            querie = queries[i]
            nb_hits = len(query_result.hits) if query_result.hits else 0
            querie_offset = querie.offset or 0
            querie_limit = querie.limit or 10

            if query_result.estimated_total_hits is not None and nb_hits < (
                query_result.estimated_total_hits - querie_offset
            ):
                querie.offset = querie_offset + querie_limit
                querie.limit = query_result.estimated_total_hits - nb_hits
                next_queries.append(querie)

        if next_queries:
            new_result = self.recursive_smart_multi_search(next_queries, cached_session)

            if new_result and new_result.results:
                for i in range(len(new_result.results)):
                    query_result = new_result.results[i]
                    hits_list = result.results[i].hits
                    if query_result.hits and hits_list is not None:
                        hits_list.extend(query_result.hits)
        return result

    def recursive_multi_search(
        self,
        queries: Sequence[MultiSearchQuery] | None = None,
        cached_session: CachedSession | None = None,
    ) -> MultiSearchResults | None:
        """Alias for recursive_smart_multi_search for backward compatibility."""
        return self.recursive_smart_multi_search(queries, cached_session)
