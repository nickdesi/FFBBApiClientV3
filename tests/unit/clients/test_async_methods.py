import pytest
import httpx
import respx
from ffbb_api_client_v3.clients.api_ffbb_app_client import ApiFFBBAppClient
from ffbb_api_client_v3.models.live import Live

@pytest.mark.asyncio
async def test_get_lives_async():
    client = ApiFFBBAppClient(bearer_token="test-token", debug=True)
    
    with respx.mock:
        route = respx.get("https://api.ffbb.app/json/lives.json").respond(
            json=[{
                "matchId": 1, 
                "competitionName": "Match 1", 
                "currentStatus": "en_cours"
            }]
        )
        
        lives = await client.get_lives_async()
        assert lives is not None
        assert len(lives) == 1
        assert lives[0].match_id == 1
        assert lives[0].competition_name == "Match 1"

@pytest.mark.asyncio
async def test_get_competition_async():
    client = ApiFFBBAppClient(bearer_token="test-token", debug=True)
    
    with respx.mock:
        # Use a regex match to handle the complex query parameters
        route = respx.get(url__startswith="https://api.ffbb.app/items/ffbbserver_competitions/123").respond(
            json={"data": {"id": "123", "nom": "Coupe de France"}}
        )
        
        comp = await client.get_competition_async(123)
        assert comp is not None
        assert comp.id == "123"
        assert comp.nom == "Coupe de France"
