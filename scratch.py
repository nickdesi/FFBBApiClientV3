from ffbb_api_client_v3.helpers.meilisearch_client_extension import (
    MeilisearchClientExtension,
)


class FakeMeilisearchClientExtension(MeilisearchClientExtension):
    def multi_search(self, queries, cached_session=None):
        pass
