import httpx
headers = {"user-agent": "okhttp/4.12.0"}
r = httpx.get("https://api.ffbb.app/items/configuration", headers=headers)
data = r.json().get("data", {})
token = data.get("api_bearer_token")

headers["Authorization"] = f"Bearer {token}"
collections = [
    "ffbbserver_organismes",
    "ffbbserver_competitions",
    "ffbbserver_poules",
    "ffbbserver_saisons"
]

results = {}
for c in collections:
    r_test = httpx.get(f"https://api.ffbb.app/items/{c}?limit=1", headers=headers)
    results[c] = r_test.status_code

print(results)
