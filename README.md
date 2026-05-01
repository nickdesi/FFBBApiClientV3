<div align="center">

# 🏀 FFBB API Python Client V3

**SDK Python moderne, typé et asynchrone pour exploiter les données publiques FFBB : clubs, compétitions, rencontres, classements, salles, officiels et recherche Meilisearch.**

[![PyPI](https://img.shields.io/pypi/v/ffbb_api_client_v3?color=blue&label=PyPI&logo=python)](https://pypi.org/project/ffbb_api_client_v3/)
[![Python](https://img.shields.io/pypi/pyversions/ffbb_api_client_v3?logo=python)](https://pypi.org/project/ffbb_api_client_v3/)
[![CI](https://github.com/nickdesi/FFBBApiClientV3/actions/workflows/ci.yml/badge.svg)](https://github.com/nickdesi/FFBBApiClientV3/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/nickdesi/FFBBApiClientV3/badge.svg?branch=master)](https://coveralls.io/github/nickdesi/FFBBApiClientV3?branch=master)
[![License](https://img.shields.io/pypi/l/ffbb_api_client_v3?color=green)](LICENSE.txt)
[![MCP-Ready](https://img.shields.io/badge/MCP-Ready-orange.svg?logo=modelcontextprotocol)](https://github.com/nickdesi/FFBB-MCP-Server)

[Installation](#-installation) •
[Démarrage rapide](#-démarrage-rapide) •
[Fonctionnalités](#-fonctionnalités) •
[Recherche](#-recherche-meilisearch) •
[Async](#-utilisation-asynchrone) •
[Développement](#-développement-local)

</div>

---

## 📌 À propos

`ffbb_api_client_v3` simplifie l'accès aux API FFBB et à leurs index Meilisearch avec :

- une façade unique : `FFBBAPIClientV3` ;
- des modèles Pydantic v2 typés ;
- une API utilisable en synchrone ou en `async/await` ;
- une gestion automatique des tokens via `TokenManager` ;
- du cache HTTP configurable via `hishel` ;
- des helpers prêts pour l'intégration MCP / agents IA.

> La V3 remplace l’approche V2 basée sur des dictionnaires bruts et une configuration manuelle. Elle privilégie le typage, la robustesse réseau et les appels batchés.

---

## 🚀 Version v1.7.0 — 30 avril 2026

Principales évolutions récentes :

- ajout d'entités REST et Meilisearch : rencontres, officiels, entraîneurs, communes et assets ;
- réutilisation des clients `httpx` synchrones et asynchrones ;
- cache Meilisearch optimisé pour limiter les copies coûteuses ;
- retries de transport configurables via `CacheConfig.transport_retries` ;
- mise à jour des schémas OpenAPI, collections et index ;
- stabilisation CI, typage, tests et formatage.

Voir aussi : [`CHANGELOG.md`](CHANGELOG.md) et [`RELEASE_NOTES.md`](RELEASE_NOTES.md).

---

## 📦 Installation

```bash
pip install ffbb_api_client_v3
```

Pour contribuer ou exécuter les tests :

```bash
git clone https://github.com/nickdesi/FFBBApiClientV3.git
cd FFBBApiClientV3
pip install -e ".[testing]"
```

Prérequis : Python `>=3.10`.

---

## ⚡ Démarrage rapide

```python
from ffbb_api_client_v3 import FFBBAPIClientV3

client = FFBBAPIClientV3.create()

# Recherche globale sur les index FFBB
results = client.multi_search("Pau Orthez")

for result in results or []:
    print(result.index_uid, len(result.hits or []))

# Lives en cours
lives = client.get_lives()
```

`FFBBAPIClientV3.create()` résout automatiquement les tokens si aucun token n'est passé explicitement.

---

## ✨ Fonctionnalités

| Domaine | Capacités |
|---|---|
| API FFBB | clubs, compétitions, organismes, saisons, poules, classements, rencontres, lives |
| Recherche | organismes, compétitions, rencontres, salles, terrains, pratiques, tournois, engagements et formations |
| REST typé | récupération de ressources individuelles avec modèles Pydantic v2 |
| Async | méthodes `*_async()` pour les appels réseau non bloquants |
| Cache | cache HTTP `hishel`, sessions `httpx` réutilisées, retries configurables |
| Sécurité | masquage des tokens dans les logs |
| IA / MCP | structure compatible avec des wrappers MCP et agents IA |

---

## 🔍 Recherche Meilisearch

### Recherche globale

```python
results = client.multi_search("Clermont")
```

### Recherche ciblée

```python
organismes = client.search_organismes(
    "Clermont",
    filter=['codePostal = "63000"'],
    sort=["nom:asc"],
    limit=10,
)

rencontres = client.search_rencontres("N1M", limit=20)
salles = client.search_salles("Maison des Sports", limit=5)
engagements = client.search_engagements("U15M", limit=20)
```

### Recherche géographique

```python
clubs = client.search_organismes_by_geo(
    lat=45.7772,
    lng=3.0870,
    radius_km=20,
    limit=20,
)
```

### Principales méthodes exposées

| Ressource | Méthode sync | Méthode async |
|---|---|---|
| Recherche globale | `multi_search()` | `multi_search_async()` |
| Clubs / organismes | `search_organismes()` | `search_organismes_async()` |
| Compétitions | `search_competitions()` | `search_competitions_async()` |
| Rencontres | `search_rencontres()` | `search_rencontres_async()` |
| Salles | `search_salles()` | `search_salles_async()` |
| Terrains | `search_terrains()` | `search_terrains_async()` |
| Pratiques | `search_pratiques()` | `search_pratiques_async()` |
| Tournois | `search_tournois()` | `search_tournois_async()` |
| Engagements | `search_engagements()` | `search_engagements_async()` |
| Formations | `search_formations()` | `search_formations_async()` |

---

## 🧱 Accès REST typé

```python
# Ressources principales
organisme = client.get_organisme(12345)
competition = client.get_competition(67890)
poule = client.get_poule(11111)

# Ressources ajoutées récemment
rencontre = client.get_rencontre(22222)
officiel = client.get_officiel(33333)
entraineur = client.get_entraineur(44444)
```

Les assets Directus et autres collections peuvent être exploités via les méthodes REST/listing dédiées exposées par le client lorsque disponibles.

Les réponses sont converties en modèles Pydantic lorsque le schéma est connu, ce qui apporte validation, autocomplétion et sérialisation propre.

---

## 🧵 Utilisation asynchrone

```python
import asyncio
from ffbb_api_client_v3 import FFBBAPIClientV3

async def main() -> None:
    client = FFBBAPIClientV3.create()

    results = await client.search_organismes_async("ASVEL")
    lives = await client.get_lives_async()

    print(results.estimated_total_hits if results else 0)
    print(len(lives or []))

asyncio.run(main())
```

---

## 🔐 Tokens et configuration

Par défaut, le client utilise `TokenManager.get_tokens()` au moment de la création :

```python
from ffbb_api_client_v3 import FFBBAPIClientV3, TokenManager

tokens = TokenManager.get_tokens()

client = FFBBAPIClientV3.create(
    api_bearer_token=tokens.api_token,
    meilisearch_bearer_token=tokens.meilisearch_token,
)
```

Il est donc possible de laisser le client résoudre les tokens automatiquement ou de les fournir explicitement selon le contexte d'exécution.

---

## 🏗 Architecture

```text
src/ffbb_api_client_v3/
├── clients/
│   ├── ffbb_api_client_v3.py       # Façade publique
│   ├── api_ffbb_app_client.py      # Client REST FFBB
│   └── meilisearch_ffbb_client.py  # Client recherche Meilisearch
├── helpers/                        # Requêtes HTTP, multi-search, conversions
├── models/                         # Modèles Pydantic v2
├── utils/                          # cache, tokens, logging sécurisé
└── data/                           # schémas et métadonnées embarqués
```

---

## 🧪 Développement local

```bash
pip install -e ".[testing]"
pytest tests/
```

Commandes utiles :

```bash
pytest tests/unit/
pytest tests/integration/
pytest tests/ --cov=src
```

Documentation complémentaire :

- [`LOCAL_CI_GUIDE.md`](LOCAL_CI_GUIDE.md)
- [`docs/testing_conventions.md`](docs/testing_conventions.md)
- [`docs/architecture.rst`](docs/architecture.rst)

---

## 🤖 Intégration IA / MCP

Le client sert de base au serveur MCP FFBB et expose une API stable pour construire des outils agent-friendly : recherche de clubs, récupération de poules, classements, lives, calendriers et détails de rencontres.

Projet associé : [FFBB-MCP-Server](https://github.com/nickdesi/FFBB-MCP-Server)

---

## 🤝 Contribuer

Les contributions sont bienvenues :

- ouvrez une [issue](https://github.com/nickdesi/FFBBApiClientV3/issues) pour un bug ;
- proposez une évolution via les [discussions](https://github.com/nickdesi/FFBBApiClientV3/discussions) ;
- lancez les tests localement avant une pull request.

---

## 📄 Licence

Distribué sous licence Apache-2.0. Voir [`LICENSE.txt`](LICENSE.txt).

---

<div align="center">

**Si ce projet vous aide, une étoile est appréciée. ⭐**

[![GitHub stars](https://img.shields.io/github/stars/nickdesi/FFBBApiClientV3?style=social)](https://github.com/nickdesi/FFBBApiClientV3/stargazers)

</div>
