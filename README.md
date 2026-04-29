<div align="center">

# 🏀 FFBB API Python Client V3

**Le SDK Python moderne, typé et industriel pour toutes les API et statistiques de la Fédération Française de Basketball.**

[![PyPI](https://img.shields.io/pypi/v/ffbb_api_client_v3?color=blue&label=PyPI&logo=python)](https://pypi.org/project/ffbb_api_client_v3/)
[![Python](https://img.shields.io/pypi/pyversions/ffbb_api_client_v3?logo=python)](https://pypi.org/project/ffbb_api_client_v3/)
[![CI](https://github.com/nickdesi/FFBBApiClientV3/actions/workflows/ci.yml/badge.svg)](https://github.com/nickdesi/FFBBApiClientV3/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/nickdesi/362a9a7a9a7a9a7a9a7a/raw/covbadge.json)](https://github.com/nickdesi/FFBBApiClientV3)
[![License](https://img.shields.io/pypi/l/ffbb_api_client_v3?color=green)](LICENSE.txt)
[![MCP-Ready](https://img.shields.io/badge/MCP-Ready-orange.svg?logo=modelcontextprotocol)](https://github.com/nickdesi/FFBB-MCP-Server)

[🚀 Quick Start](#-quick-start) •
[✨ Fonctionnalités](#-fonctionnalités) •
[🔍 Meilisearch](#-9-index-meilisearch) •
[🤖 IA / MCP](#-intégration-ia--mcp) •
[🚢 Architecture](#-architecture) •
[🤝 Contribuer](#-contribuer)

---

> **Note:** Ce SDK est une refonte totale de la V2. Il est pensé pour la performance, le typage strict avec Pydantic v2, et une intégration native avec les agents IA via le protocole MCP.

</div>

---

## ⚡ Pourquoi V3 ?

L'API FFBB est complexe : tokens à renouveler, 9 index de recherche séparés, données imbriquées. La V3 automatise tout cela pour vous permettre de vous concentrer sur votre application.

| Feature | FFBB Client V2 | FFBB Client V3 | Gain |
|---|---|---|---|
| **Tokens** | Manuels / `os.getenv` | **Auto-résolus (`TokenManager`)** | ⚡ Zéro configuration |
| **Typage** | `dict` bruts | **70+ modèles Pydantic v2** | 🛠️ Autocomplétion totale |
| **Recherche** | 1 appel par type | **1 `multi_search` (9 index)** | 🚀 -90% de latence |
| **Async** | Partiel | **Natif (`httpx`)** | 💨 Performance I/O |
| **Cache** | Manuel | **Intégré (`hishel`)** | 📉 Quotas préservés |
| **IA** | ❌ | **✅ MCP-ready** | 🤖 Claude/Cursor compatible |

---

## 🚀 Quick Start

### Installation

```bash
pip install ffbb_api_client_v3
```

### Usage Express (Zéro Configuration)

Plus besoin de chercher vos tokens. Le client les résout automatiquement au premier appel.

```python
from ffbb_api_client_v3 import FFBBAPIClientV3

# Initialisation instantanée
client = FFBBAPIClientV3.create()

# Recherche sur les 9 index (Clubs, Matchs, Salles, etc.)
results = client.multi_search("Pau Orthez")

# Accès typé avec autocomplétion
for hit in results[0].hits:
    print(f"🏀 {hit.nom} ({hit.ville})")

# Récupérer les lives en cours
lives = client.get_lives()
```

---

## ✨ Fonctionnalités

- 🏀 **API FFBB complète** — clubs, compétitions, saisons, poules, classements, lives, **rencontres, officiels, entraîneurs, communes, assets**
- 🔍 **9 index Meilisearch** — `filter`, `sort`, `limit` natifs sur toutes les méthodes
- ⚡ **Sync + Async** — chaque méthode disponible en `async/await`
- 🧩 **60+ modèles Pydantic v2** — type-safe, validation, sérialisation
- 📦 **Cache HTTP intégré** — SQLite ou mémoire via `hishel[async]`, configurable
- 🔄 **Retry + Timeout** — robustesse réseau out-of-the-box
- 🔐 **TokenManager intelligent** — auto-résolution + renouvellement transparent
- 🪵 **Logging sécurisé** — tokens masqués automatiquement dans les logs
- 🤖 **MCP-ready** — wrapper officiel pour Claude, Cursor, Copilot
- 🧪 **400+ tests** — unitaires + intégration, CI GitHub Actions

---

## 🔍 9 Index Meilisearch

```python
# 1 appel réseau → 9 index interrogés simultanément
results = client.multi_search("Clermont")

# Filtrage natif
organismes = client.search_organismes(
    "Clermont",
    filter=['codePostal = "63000"'],
    sort=["nom:asc"],
    limit=10,
)

# Nouveaux index REST associés
rencontres = client.search_rencontres("N1M", limit=20)
officiels = client.search_officiels("Dupont")
entraineurs = client.search_entraineurs("Durand")
communes = client.search_communes("Clermont-Ferrand")
```

| Index | Sync | Async | Description |
|---|---|---|---|
| `ffbbserver_organismes` | `search_organismes()` | `…_async()` | Clubs, comités, ligues |
| `ffbbserver_competitions` | `search_competitions()` | `…_async()` | Compétitions officielles |
| `ffbbserver_rencontres` | `search_rencontres()` | `…_async()` | Matchs et rencontres |
| `ffbbserver_officiels` | `search_officiels()` | `…_async()` | Arbitres et officiels |
| `ffbbserver_entraineurs` | `search_entraineurs()` | `…_async()` | Entraîneurs |
| `ffbbserver_communes` | `search_communes()` | `…_async()` | Communes |
| `ffbbserver_salles` | `search_salles()` | `…_async()` | Salles et gymnases |
| `ffbbserver_pratiques` | `search_pratiques()` | `…_async()` | Lieux de pratique |
| `ffbbserver_terrains` | `search_terrains()` | `…_async()` | Terrains basket |
| `ffbbserver_tournois` | `search_tournois()` | `…_async()` | Tournois |
| `ffbbserver_engagements` | `search_engagements()` | `…_async()` | Engagements équipes ✨ v1.5 |
| `ffbbserver_formations` | `search_formations()` | `…_async()` | Formations & stages ✨ v1.5 |

---

## 🧱 Nouveaux modèles & endpoints REST
officiel = client.get_officiel(id_officiel)

### Nouveaux Endpoints — Explication concise

Voici ce que fournissent concrètement les nouveaux endpoints intégrés :

- **Rencontres (`items/ffbbserver_rencontres`)** : données détaillées sur un match/rencontre
    - usages : récupérer une rencontre par `id`, afficher score, équipes, lieu, date, feuille de match
    - modèle : `get_rencontre_response.py` (wrapper REST typé)

- **Officiels (`items/ffbbserver_officiels`)** : arbitres et officiels liés aux rencontres
    - usages : récupérer un officiel par `id`, consulter ses informations de carrière, licences, rôle (arbitre, commissaire)
    - modèle : `get_officiel_response.py`

- **Entraîneurs (`items/ffbbserver_entraineurs`)** : profils entraîneurs
    - usages : récupérer un entraîneur par `id`, affichage club(s) associés, licence, historique
    - modèle : `get_entraineur_response.py`

- **Communes (`items/ffbbserver_communes`)** : index géographique léger
    - usages : recherche de communes (nom, code postal), résolution d'adresse pour affichage de salles/terrains
    - accessible principalement via les méthodes `search_communes()` / `search_communes_async()`

- **Assets (Directus files)** : fichiers et images servis via Directus
    - usages : construction d'URLs d'assets (`get_asset_url(uuid, width, height, format, quality)`) pour thumbnails et affichage optimisé

Ces endpoints existent à la fois en recherche Meilisearch (pour listes / recherche texte) et en REST (pour ressources individuelles). Les principaux points d'accès sont :

```python
from ffbb_api_client_v3 import FFBBAPIClientV3, TokenManager

tokens = TokenManager.get_tokens()
client = FFBBAPIClientV3.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
)

# Récupérer une rencontre (REST typé)
rencontre = client.get_rencontre(12345)

# Récupérer un officiel
officiel = client.get_officiel(9876)

# Rechercher des entraîneurs via Meilisearch
res = client.search_entraineurs("Durand", limit=5)

# Construire une URL d'asset optimisée
img = client.get_asset_url(uuid="...", width=800, height=600, format="webp", quality=80)
```

Note : `API_FFBB_COM_BASE_URL` est commenté temporairement dans `config.py` en
attente d'une possible migration de domaine côté FFBB — le client prend en
charge ce changement sans breaking change exposé dans l'API publique.

---

## 🚢 Architecture & Qualité

```text
src/ffbb_api_client_v3/
├── clients/
│   ├── ffbb_api_client_v3.py       # Façade — Point d'entrée unique
│   ├── api_ffbb_app_client.py      # Client REST (httpx)
│   └── meilisearch_ffbb_client.py  # Client Recherche
├── models/                         # 70+ modèles Pydantic v2
├── utils/
│   ├── token_manager.py            # Résolution auto des secrets
│   ├── cache_manager.py            # Gestionnaire de cache hishel
│   └── secure_logging.py           # Masquage des tokens
└── helpers/                        # Utilitaires HTTP et Multi-search
```

### Pipeline de Release Automatisé
Le projet utilise **OIDC Trusted Publisher** pour PyPI et un pipeline CI/CD complet :
- ✅ **Tests unitaires & intégration** (400+ tests)
- ✅ **Parity Check** hebdomadaire via analyse AST
- ✅ **Release auto** sur tag git avec génération de notes
- ✅ **Sync auto** avec le serveur MCP

---

## 🛠 Développement Local

Consultez le **[Guide CI Local](LOCAL_CI_GUIDE.md)** pour configurer votre environnement de test.

```bash
git clone https://github.com/nickdesi/FFBBApiClientV3.git
pip install -e ".[testing]"
pytest tests/ --cov=src   # Exécuter les tests avec couverture
```

---

## 🤝 Contribuer

Les contributions sont les bienvenues !
- Pour les bugs, ouvrez une **[Issue](https://github.com/nickdesi/FFBBApiClientV3/issues)**.
- Pour les nouvelles fonctionnalités, passez par les **[Discussions](https://github.com/nickdesi/FFBBApiClientV3/discussions)**.

---

<div align="center">

**Si ce projet vous aide, n'oubliez pas de lui donner une étoile ! ⭐**

[![GitHub stars](https://img.shields.io/github/stars/nickdesi/FFBBApiClientV3?style=social)](https://github.com/nickdesi/FFBBApiClientV3/stargazers)

</div>
