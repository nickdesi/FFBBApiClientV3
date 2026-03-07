# FFBB API Client V3

<!-- Badges existants (à mettre à jour avec vos URLs exactes si nécessaire) -->
[![PyPI-Server](https://img.shields.io/pypi/v/ffbb_api_client_v3.svg)](https://pypi.org/project/ffbb_api_client_v3/)
[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

**FFBBApiClientV3_Python** est une librairie client moderne en Python destinée à interagir de façon transparente avec les nouvelles API de la Fédération Française de Basketball (FFBB).
Elle fournit une interface complète et typée (via Pydantic) pour récupérer les informations concernant les clubs, les équipes, les compétitions, les matchs, les saisons, et bien plus encore.

## Fonctionnalités Principales

- 🏀 **Couverture Complète de l'API** : Accédez à tous les services de la FFBB (compétitions, organismes, saisons, matchs en direct, recherche globale).
- 🔧 **Modèles Typés (Type-Safe)** : Modèles de données fortement typés avec validation automatique et gestion d'erreurs (via Pydantic).
- 🎯 **Sélection Dynamique des Champs** : Personnalisez vos requêtes pour obtenir les champs essentiels (BASIC), standards (DEFAULT) ou complets (DETAILED) pour des appels API optimisés.
- 📦 **Architecture Moderne** : Un code propre et modulaire, pensé pour une grande facilité de maintenance et d'évolution.
- ⚡ **Mise en Cache Intégrée** : Support de cache asynchrone natif (`hishel`, `requests-cache`) pour améliorer les performances de façon drastique.
- 🧪 **Excellente Couverture de Tests** : Des tests unitaires et d'intégration complets garantissant une très haute fiabilité.

---

## Tech Stack

- **Langage** : Python 3.10+
- **Requêtes HTTP** : `httpx` (pour l'asynchrone et synchrone)
- **Validation des données** : `pydantic` >= 2.0.0
- **Gestion du Cache** : `hishel` >= 0.0.32
- **Gestion des Environnements** : `python-dotenv`
- **Tests** : `pytest` (avec `pytest-asyncio`, `pytest-cov`, `respx`)

---

## Prérequis

- Python 3.10 ou version ultérieure installé sur votre machine.
- Pip (ou un équivalent moderne comme `uv` ou `poetry`).
- (*Optionnel*) Un jeton applicatif de la FFBB (si votre usage dépasse les accès publics fournis par défaut).

---

## 🚀 Getting Started (Guide de démarrage rapide)

### 1. Installation

Installez directement le package depuis PyPI :

```bash
pip install ffbb_api_client_v3
```

### 2. Configuration de l'environnement

Bien que le client gère automatiquement la récupération des tokens publics, il est fortement recommandé de configurer vos propres variables d'environnement.

Créez un fichier `.env` à la racine de votre projet :

```bash
# Fichier .env
API_FFBB_APP_BEARER_TOKEN=votre_token_api_ffbb_ici
MEILISEARCH_BEARER_TOKEN=votre_token_meilisearch_ici
```

### 3. Utilisation Simplifiée (Quick Start)

Voici comment initialiser le client et effectuer vos premières recherches :

```python
from ffbb_api_client_v3 import FFBBAPIClientV3, TokenManager

# Résolution automatique du token (via variables d'environnement ou endpoint public FFBB)
tokens = TokenManager.get_tokens()

# Initialisation du client
client = FFBBAPIClientV3.create(
    api_bearer_token=tokens.api_token,
    meilisearch_bearer_token=tokens.meilisearch_token
)

# Exemple 1 : Rechercher les organisations dans une ville
organismes = client.search_organismes("Paris")
print(f"Trouvé {len(organismes.hits)} organismes à Paris.")

# Obtenir des informations détaillées sur le premier organisme trouvé
if organismes.hits:
    organisme_id = int(organismes.hits[0].id)
    organisme_details = client.get_organisme(organisme_id)
    print(f"Organisme : {organisme_details.nom}")
    print(f"  - Adresse : {organisme_details.adresse}")
    print(f"  - Équipes engagées : {len(organisme_details.engagements)}")

# Exemple 2 : Obtenir les matchs en direct (Lives)
lives = client.get_lives()
print(f"Matchs actuellement en direct : {len(lives)}")
```

---

## 🏗 Architecture du Projet

La solution est soigneusement segmentée en plusieurs couches pour une intégration et une lisibilité parfaite.

### Structure des Dossiers (`src/ffbb_api_client_v3`)

```text
src/
└── ffbb_api_client_v3/
    ├── clients/          # Classes d'interfaçage HTTP avec les API FFBB
    │   ├── api_ffbb_app_client.py     # Opérations de lecture standards (get)
    │   ├── meilisearch_ffbb_client.py # Opérations de recherche (Meilisearch)
    │   └── ffbb_api_client_v3.py      # Façade principale (Client Maître) réunissant les autres
    ├── models/           # Modèles Pydantic définissant la structure exacte des données (Type-Safe)
    │   ├── get_organisme_response.py
    │   ├── competitions_models.py
    │   └── query_fields.py            # Gestionnaire de champs GraphQL-like (BASIC, DETAILED, etc.)
    ├── helpers/          # Utilitaires pour formater, étendre ou simplifier les retours de l'API
    ├── utils/            # Classes support (TokenManager, CacheManager, Logger)
    └── config.py         # Configuration par défaut (URLs de la FFBB, etc.)
```

### Concepts Clés

#### Gestion Personnalisée des Champs (Fields)

Afin d'éviter d'interroger la base de données FFBB pour des données inutiles, vous pouvez piloter les champs exacts à récupérer :

```python
from ffbb_api_client_v3.models.query_fields import QueryFieldsManager, FieldSet

# Charger le modèle uniquement avec les informations de base
basic_fields = QueryFieldsManager.get_organisme_fields(FieldSet.BASIC)
organisme = client.get_organisme(
    organisme_id=12345,
    fields=basic_fields
)
```

#### Moteur de Recherche Multi-ressources

L'API de recherche FFBB est propulsée par un Meilisearch distant extrêmement rapide :

```python
# Recherche unifiée sur tous les sujets relatifs à 'Lyon' (Clubs, Salles, Matchs, etc.)
results = client.multi_search("Lyon")
for result in results:
    print(f"Trouvé : {result.query} (Type : {type(result).__name__})")
```

---

## 🔐 Variables d'Environnement

Voici le détail des variables d'environnement supportées via `python-dotenv`.

| Variable | Description | Source |
| --- | --- | --- |
| `API_FFBB_APP_BEARER_TOKEN` | Token d'accès à l'API Rest FFBB | FFBB Settings |
| `MEILISEARCH_BEARER_TOKEN` | Token d'accès au cluster Meilisearch public de la FFBB | FFBB Settings |
| `FFBB_API_BASE_URL` | *Optionnel* - Base URL racine pour l'API REST `api.ffbb.app` | Par défaut géré |
| `FFBB_MEILI_BASE_URL` | *Optionnel* - Base URL racine pour Meilisearch | Par défaut géré |

> 💡 **Astuce** : `TokenManager` peut, lors de l'exécution, extraire dynamiquement les clés d'Auth des endpoints de configuration applicative de la FFTB, sans action de votre part, mais en production, il est recommandé de les "hardcoder" comme variables d'environnement pour gagner en robustesse.

---

## 🛠 Available Scripts (Pour le développement local)

Si vous souhaitez contribuer ou forker cette librairie afin de l'étendre localement, voici les commandes utiles :

| Commande | Description |
| --- | --- |
| `pip install -e .[testing]` | Installe la librairie en mode développeur avec les dépendances de test. |
| `tox` | Lance tous les tests et la vérification de conformité complète de la librairie. |
| `pytest` | Lance l'ensemble de la suite de tests (située dans `tests/`). |
| `pylint src/` | Exécute l'analyse statique du code selon les conventions. |
| `./run-ci-locally.sh` | Lance un script Bash local simulant l'environnement Github Actions. |

---

## 🧪 Tests (QA)

Ce projet exige de maintenir une très haute fiabilité face aux changements des interfaces publiques de la FFBB.

### Exécuter la Suite de Tests

```bash
# Tests unitaires purs (sans appels réseau)
python -m unittest tests.test_001_unit_tests_core -v

# Tests d'intégration avancés (nécessitent de bons tokens de développement)
python -m unittest tests.test_011_enhanced_integration -v

# Découverte automatique et couverture globale
pytest --cov=src tests/
```

### Architecture des Tests

```text
tests/
├── test_001_unit_tests_core.py        # Opérations de base, mocks et validations Pydantic
├── test_005_integration_user_journey.py # Tests réels du bout en bout
└── test_011_enhanced_integration.py     # Intégrations avancées sur le moteur de recherche
```

---

## ☁️ Utilisation en Déploiement / Production

Étant une librairie (SDK), `ffbb_api_client_v3` s'intègre naturellement dans n'importe quel écosystème Dockerisé ou serverless Python (FastAPI, Django, AWS Lambda, Cloud Run).

### Exemple d'intégration `requirements.txt`

```text
ffbb_api_client_v3>=1.0.0
```

### Exemple dans un `Dockerfile` (FastAPI)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
# La librairie ffbb_api_client_v3 sera installée ici.

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Conseils de production :**

- Utilisez `FFBBAPIClientV3.create()` avec un jeu de token fixes via le `TokenManager` pour éviter d'appeler l'endpoint de configuration FFBB à chaque boot du serveur.
- Laissez le `CacheManager` par défaut de la librairie faire son travail (ou surchargez-le avec `redis` ou autre si vous utilisez `hishel` pour persister le cache sur des pods multi-instances).

---

## 🚑 Troubleshooting (Dépannage)

### Erreur : `401 Unauthorized` ou `Forbidden`

**Solution :**
Les tokens de l'API FFBB et de Meilisearch tendent à expirer.
Exécutez un vidage de cache ou forcez un rafraîchissement des tokens:

```python
from ffbb_api_client_v3 import TokenManager
tokens = TokenManager.get_tokens(use_cache=False)
```

### Erreur de Pydantic : `ValidationError` (Champs manquants)

L'API de la FFBB évolue et de nouveaux champs (ou des suppressions) peuvent apparaître sur le retour JSON.
**Solution :**

- Assurez-vous d'utiliser la dernière version du Package.
- Modifiez les configurations GraphQL de base encapsulées dans `QueryFieldsManager` pour désactiver le champ fautif.

### Mise en cache persistante

Si vous obtenez des données qui n'évoluent pas entre deux appels (ex: anciens scores d'un live) :

```python
from ffbb_api_client_v3.utils.cache_manager import CacheManager
# Vider manuellement le cache
CacheManager().clear()
```

---

## 📄 Licence

`ffbb_api_client_v3` est distribué sous la licence [Apache 2.0](LICENSE.txt).

---

## Remerciements / Dev Notes

Cette architecture de code a été générée via l'outil PyScaffold 4.6.
Pour plus de détails : <https://pyscaffold.org/>
