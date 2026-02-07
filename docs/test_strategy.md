# Test Strategy - FFBBApiClientV2_Python

## 1. Pyramide des tests

### Niveau 1 : Unit - Edge cases `from_dict`
Tests unitaires avec donnees limites (None, dict vide, erreurs API, types invalides).
Pas d'appels reseau, execution instantanee.

**Fichier** : `tests/test_021_raw_json_model_conversion.py` (Section C, tests 020-036)

### Niveau 1b : Unit - Round-trip `from_dict` -> `to_dict`
Tests de stabilite double round-trip : `from_dict(to_dict(from_dict(data)))` doit etre stable.
Couvre toutes les methodes `to_dict()` des modeles.

**Fichier** : `tests/test_022_to_dict_round_trip.py` (38 tests, tous passing)

### Niveau 2 : Unit - `from_dict` avec fixtures JSON statiques
Tests avec fichiers JSON statiques captures depuis l'API reelle.
Couverture champ par champ offline.

**Status** : A implementer (voir Recommandations futures)

### Niveau 3 : Integration - API brute (raw HTTP + from_dict)
Appels HTTP directs avec `requests` sans passer par les clients du projet.
Validation de la conversion JSON brut -> modeles.

**Fichier** : `tests/test_021_raw_json_model_conversion.py` (Sections A et B, tests 001-017)

### Niveau 4 : Integration - Via clients du projet
Tests des clients `ApiFFBBAppClient` et `MeilisearchFFBBClient`.

**Fichiers** : `test_000` a `test_005`, `test_010`, `test_011`

### Niveau 5 : E2E - Parcours utilisateur complets
Scenarios multi-etapes (recherche -> club -> equipes -> calendrier).

**Fichier** : `test_010_integration_user_journey.py`

---

## 2. Matrice de couverture

| Modele | Niveau 1 (edge) | Niveau 3 (raw HTTP) | Niveau 4 (client) | Couverture |
|--------|:---:|:---:|:---:|:---:|
| `GetSaisonsResponse` | x | x | x | **100%** |
| `GetCompetitionResponse` | x | x | x | 91% |
| `GetOrganismeResponse` | x | x | x | 92% |
| `GetPouleResponse` | x | x | x | **95%** |
| `GetConfigurationResponse` | x | x | x | **100%** |
| `GameStatsModel` | x | - | - | **100%** |
| `TeamRanking` | x | x (via poule) | x | **100%** |
| `RankingEngagement` | x | x (via poule) | x | **100%** |
| `Live` / `Clock` | x | x | x | **93%** |
| `NiveauExtractor` | x | - | - | **95%** |
| `CompetitionsMultiSearchResult` | x | x | x | **92%** |
| `OrganismesMultiSearchResult` | x | x | x | **91%** |
| `SallesMultiSearchResult` | x | x | x | **92%** |
| `TerrainsMultiSearchResult` | x | x | x | 71% (*) |
| `RencontresMultiSearchResult` | x | x | x | 87% |
| `PratiquesMultiSearchResult` | x | x | x | 75% |
| `TournoisMultiSearchResult` | x | x | x | 83% |
| `MultiSearchResults` | x | x | x | **98%** |

(*) Bug DocumentFlyer corrige : `FacetStats.from_dict` levait `NotImplementedError` non capture par `from_union` → remplace par `assert False` (capture par `from_union`).

---

## 3. Analyse de couverture

### Avant ajout des tests (baseline)
- **Couverture globale** : 62% (6062 stmts, 1635 miss)
- **Tests** : 172

### Apres ajout test_021 (raw JSON conversion)
- **Couverture globale** : 64% (6062 stmts, 1547 miss)
- **Tests** : 204 (+32 nouveaux)

### Apres ajout test_022 (round-trip to_dict)
- **Couverture globale** : **81%** (6062 stmts, 782 miss)
- **Tests** : 242 (+38 nouveaux, dont 2 skipped)

### Apres ajout test_023 a test_045 (modeles, client, helpers)
- **Couverture globale** : **92%** (6062 stmts, 489 miss)
- **Tests** : 346 (+104 nouveaux, 0 skipped)
- Bugs corriges : FacetStats.from_dict (`assert False` au lieu de `raise NotImplementedError`), IDEngagementEquipe.to_dict (`to_class` au lieu de `from_dict`)

### Gains principaux (baseline 62% -> 92%)
| Module | Baseline | Apres test_021 | Apres test_022 | Delta total |
|--------|:--------:|:--------------:|:--------------:|:-----------:|
| `game_stats_models.py` | 71% | **100%** | **100%** | +29 |
| `rankings_models.py` | 83% | **100%** | **100%** | +17 |
| `saisons_models.py` | 76% | **100%** | **100%** | +24 |
| `niveau_models.py` | 36% | **95%** | **95%** | +59 |
| `poules_models.py` | 86% | **95%** | **95%** | +9 |
| `competitions_models.py` | 88% | 91% | 91% | +3 |
| `organismes_models.py` | 86% | 92% | 92% | +6 |
| `multi_search_result_competitions.py` | ~47% | ~47% | **92%** | +45 |
| `multi_search_result_organismes.py` | ~54% | ~54% | **91%** | +37 |
| `multi_search_result_salles.py` | ~55% | ~55% | **92%** | +37 |
| `multi_search_result_rencontres.py` | ~54% | ~54% | 87% | +33 |
| `multi_search_result_tournois.py` | ~56% | ~56% | 83% | +27 |
| `multi_search_result_pratiques.py` | ~52% | ~52% | 75% | +23 |
| `lives.py` | ~50% | ~50% | **93%** | +43 |
| `affiche.py` | ~50% | ~50% | **98%** | +48 |
| `nature_sol.py` | ~50% | ~50% | **91%** | +41 |
| `multi_search_results_class.py` | ~56% | ~56% | **98%** | +42 |

### Objectif 90% atteint (92%)
Tous les gaps identifies ont ete couverts :

1. **`document_flyer.py`** : 19% → couvert (bug FacetStats corrige, tests unskipped)
2. **`meilisearch_ffbb_client.py`** : 32% → couvert (test_040 : 21 tests mocks)
3. **`http_requests_helper.py`** / **`http_requests_utils.py`** : 36-63% → couvert (test_045 : 18 tests)
4. **`multi_search_result_pratiques.py`** : 75% → couvert (test_042 : modeles imbriques)
5. **`multi_search_result_terrains.py`** : 71% → couvert (test_041 : modeles imbriques)

---

## 4. Preconisations CI/CD

### Markers pytest

```ini
markers =
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    slow: marks tests as slow running
```

### Pipelines recommandes

| Pipeline | Commande | Frequence | Temps |
|----------|----------|-----------|-------|
| CI rapide (unit) | `pytest tests/ -m "not integration" -q -n auto` | Chaque push | ~10s |
| Integration | `pytest tests/ -q -n auto` | Nightly / pre-release | ~40s |
| Couverture | `pytest tests/ --cov=ffbb_api_client_v2 --cov-report=html -q -n auto` | Nightly | ~80s |

### Variables d'environnement requises
- `API_FFBB_APP_BEARER_TOKEN` : Token pour api.ffbb.app
- `MEILISEARCH_BEARER_TOKEN` : Token pour meilisearch-prod.ffbb.app

Les tests d'integration (Sections A et B) sont automatiquement ignores si les tokens ne sont pas definis (`@unittest.skipUnless`).

---

## 5. Recommandations futures

### A. Fixtures JSON statiques (Niveau 2)
Capturer les reponses API reelles dans `tests/fixtures/` :
```
tests/fixtures/
    saisons_response.json
    competition_12345.json
    organisme_67890.json
    meilisearch_organismes_paris.json
    ...
```
Permet des tests offline rapides avec couverture complete des champs.

### B. Snapshot testing
Installer `pytest-snapshot` pour detecter les changements de structure API :
```python
def test_organisme_snapshot(snapshot):
    result = GetOrganismeResponse.from_dict(fixture_data)
    snapshot.assert_match(asdict(result), "organisme_snapshot")
```

### C. Contract testing
Valider que les reponses API contiennent les champs attendus :
- Verifier la presence des champs requis
- Detecter les nouveaux champs non geres
- Alerter sur les champs supprimes

### D. Couverture to_dict() - FAIT
Les methodes `to_dict()` sont couvertes par `test_022_to_dict_round_trip.py`.
Technique : double round-trip `from_dict(to_dict(from_dict(data)))` stable.
**Resultat** : couverture passee de 64% a 81% (+17 points).
Bug DocumentFlyer corrige et tests unskipped (voir section 3).

### E. Mocking pour tests offline
Utiliser `responses` ou `pytest-httpserver` :
```python
@responses.activate
def test_get_saisons_offline():
    responses.get("https://api.ffbb.app/items/ffbbserver_saisons", json=fixture)
    result = client.get_saisons()
    assert len(result) > 0
```

### F. Objectif couverture 90% - FAIT
Couverture globale passee de 81% a **92%** (+11 points) :
1. Bug DocumentFlyer corrige (FacetStats `assert False`)
2. Bug IDEngagementEquipe.to_dict corrige (`to_class` au lieu de `from_dict`)
3. 23 nouveaux fichiers tests (test_023 a test_045) : modeles, client, helpers
4. 0 tests skipped (2 unskipped grace au fix FacetStats)

---

## 6. Structure des fichiers de test

| Fichier | Scope | Tests |
|---------|-------|:-----:|
| `test_000_api_ffbb_app_client.py` | Client API REST | varies |
| `test_001_unit_tests_core.py` | Tests unitaires core | varies |
| `test_002_meilisearch_client.py` | Client Meilisearch | varies |
| `test_003_meilisearch_client_extension.py` | Extension Meilisearch | varies |
| `test_004_ffbb_api_client_v2.py` | Client facade | varies |
| `test_005_integration_user_journey.py` | E2E parcours | varies |
| `test_010_integration_user_journey.py` | E2E parcours v2 | varies |
| `test_011_enhanced_integration.py` | Integration avancee | varies |
| `test_012-013` | Secure logging | varies |
| `test_014-015` | Input validation | varies |
| `test_016-017` | Retry/timeout | varies |
| `test_018` | Cache manager | varies |
| `test_019` | Config | varies |
| `test_020` | Token manager | varies |
| **`test_021_raw_json_model_conversion.py`** | **Raw JSON + from_dict** | **32** |
| **`test_022_to_dict_round_trip.py`** | **Round-trip from_dict/to_dict** | **38** |
| `test_023` a `test_039` | Round-trip modeles individuels | 34 |
| `test_040_meilisearch_ffbb_client.py` | Client Meilisearch (mocks) | 21 |
| `test_041_terrains_inner_models.py` | Modeles imbriques terrains | 6 |
| `test_042_pratiques_inner_models.py` | Modeles imbriques pratiques | 8 |
| `test_043_organisateur.py` | Organisateur round-trip | 2 |
| `test_044_competition_id.py` | CompetitionID round-trip | 2 |
| `test_045_http_helpers.py` | HTTP helpers (catch_result, etc.) | 18 |
