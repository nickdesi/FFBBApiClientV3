# Testing Conventions - FFBBApiClientV2_Python

## 1. Framework et execution

- **Style** : `unittest.TestCase` obligatoire (pas de classes bare pytest)
- **Runner** : pytest + pytest-xdist pour execution parallele
- **Commandes** :
  - Unit rapide : `python -m pytest tests/unit/ -x -q -n auto`
  - Integration : `python -m pytest tests/integration/ -q`
  - E2E : `python -m pytest tests/e2e/ -q` (necessite tokens API)
  - Couverture : `python -m pytest tests/ --cov=ffbb_api_client_v2 --cov-branch -q`

---

## 2. Organisation des repertoires

```
tests/
    conftest.py                              # Fixtures partagees (cache, env, fixture_loader)
    unit/
        models/
            test_100_categorie.py            # 1 fichier = 1 module source
            test_101_cartographie.py
            ...
        clients/
            test_200_api_ffbb_app_client.py
            test_201_unit_tests_core.py
            ...
        utils/
            test_300_secure_logging.py
            test_301_input_validation.py
            ...
        helpers/
            test_400_http_helpers.py
            ...
    integration/
        test_500_user_journey.py
        test_501_user_journey_v2.py
        ...
    e2e/
        test_600_club_lookup_journey.py
        test_601_competition_browsing_journey.py
        ...
    fixtures/
        *.json
```

---

## 3. Convention de nommage

| Element | Convention | Exemple |
|---------|-----------|---------|
| Fichier test | `test_{XXX}_{module_source}.py` | `test_100_categorie.py` |
| Classe test | `Test{ModuleSourcePascalCase}` | `TestCategorie` |
| Methode test | `test_{description_comportement}` | `test_from_dict_with_empty_dict_returns_defaults` |
| Methode helper | `_helper_name` (pas de prefixe `test_`) | `_assert_round_trip_stable` |

### Plages de numerotation {XXX}

| Plage | Categorie |
|-------|-----------|
| 100-199 | Unit - Models |
| 200-299 | Unit - Clients |
| 300-399 | Unit - Utils |
| 400-499 | Unit - Helpers |
| 500-599 | Integration |
| 600-699 | E2E |

---

## 4. Regles de qualite des tests

1. **AAA (Arrange-Act-Assert)** : chaque methode de test a 3 sections clairement separees
2. **Un acte par test** : une seule operation testee, assertions multiples acceptees si elles valident le meme resultat
3. **Isolation** : chaque test independant, `setUp()` pour etat frais, pas d'etat mutable partage entre tests
4. **Determinisme** : pas de `datetime.now()`, pas de `random`, pas de donnees live en unit tests
5. **Pas de logique** : pas de `if/for/while/try` dans les tests (utiliser `subTest()` pour iteration)
6. **Assertions explicites** : `self.assertEqual` au lieu de `assert`, `self.assertIsInstance` au lieu de `isinstance()`
7. **Nommage descriptif** : le nom de la methode decrit le comportement, pas l'implementation

---

## 5. Couverture

| Categorie | Minimum | Cible |
|-----------|---------|-------|
| Models (`from_dict`/`to_dict`) | 90% | 100% |
| Clients | 90% | 95% |
| Utils | 90% | 95% |
| Global | 90% | 97%+ |

- **Branch coverage** obligatoire (`--cov-branch`)
- Chaque module source doit avoir >= 90% de couverture individuelle

---

## 6. Tests par categorie

### Unit tests (obligatoires pour tout module)

- Round-trip `from_dict(to_dict(from_dict(data)))` stable
- `from_dict({})` : gestion des champs absents
- `from_dict(data_complete)` : tous les champs remplis
- `to_dict()` : branches `if is not None` toutes couvertes
- Forward compatibility : `from_dict` avec champs inconnus ne crash pas
- Enums : valeur de chaque membre

### Integration tests (pour clients uniquement)

- Appels API reels (skippes si tokens absents)
- Mocking HTTP avec `responses` ou `unittest.mock.patch`
- Erreurs HTTP (401, 403, 404, 429, 500)
- Timeout et erreurs reseau

### E2E tests (parcours utilisateur)

- Recherche club -> details -> equipes
- Navigation saisons -> competitions -> poules -> classement
- Recherche multi-index
- Scores en direct

---

## 7. Bonnes pratiques specifiques API client

1. **Mocker au bon niveau** : utiliser `unittest.mock.patch` avec `autospec=True`
2. **Fixtures JSON** : capturer les reponses reelles dans `tests/fixtures/`, jamais de donnees inventees
3. **Type safety** : verifier les types retournes (`assertIsInstance`), pas juste les valeurs
4. **Null safety** : chaque modele doit gerer tous les champs a `None`
5. **VCR pattern** : envisager `vcrpy` pour enregistrer/rejouer les reponses API
6. **Pas de secrets en dur** : tokens via `os.getenv()` + `skipUnless`
