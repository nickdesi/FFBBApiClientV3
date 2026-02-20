import pytest
import respx
import httpx
from ffbb_api_client_v2.helpers.meilisearch_client_extension import MeilisearchClientExtension
from ffbb_api_client_v2.models.multi_search_query import MultiSearchQuery
from ffbb_api_client_v2.models.multi_search_results_class import MultiSearchResults
from ffbb_api_client_v2.config import (
    MEILISEARCH_BASE_URL, 
    MEILISEARCH_ENDPOINT_MULTI_SEARCH,
    MEILISEARCH_INDEX_ORGANISMES
)

@pytest.mark.asyncio
async def test_smart_multi_search_async():
    client = MeilisearchClientExtension(bearer_token="test-token", url=MEILISEARCH_BASE_URL, debug=True)
    
    query_str = "paris"
    queries = [MultiSearchQuery(index_uid=MEILISEARCH_INDEX_ORGANISMES, q=query_str)]
    url = f"{MEILISEARCH_BASE_URL}{MEILISEARCH_ENDPOINT_MULTI_SEARCH}"
    
    mock_response = {
        "results": [
            {
                "indexUid": MEILISEARCH_INDEX_ORGANISMES,
                "hits": [{"id": "1", "nom": "Paris Basket"}],
                "query": query_str,
                "limit": 20,
                "offset": 0,
                "estimatedTotalHits": 1
            }
        ]
    }
    
    with respx.mock:
        respx.post(url).respond(json=mock_response)
        
        results = await client.smart_multi_search_async(queries)
        assert results is not None
        assert len(results.results) == 1
        assert results.results[0].index_uid == MEILISEARCH_INDEX_ORGANISMES
        assert len(results.results[0].hits) == 1
        assert results.results[0].hits[0].nom == "Paris Basket"
