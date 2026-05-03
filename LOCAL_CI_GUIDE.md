# Guide d'Exécution Locale des GitHub Actions

Ce guide vous explique comment répliquer et débugger vos GitHub Actions en local.

## 🎯 Objectif

Exécuter localement le même pipeline CI/CD que GitHub Actions pour :
- Débugger les erreurs avant de pousser
- Valider les changements rapidement
- Développer sans dépendre de GitHub Actions

## 📋 Prérequis

### Outils Requis
- **Python 3.11** (version utilisée par le CI)
- **tox** : `pipx install tox` ou `pip install tox`
- **pre-commit** : `pipx install pre-commit` ou `pip install pre-commit`

### Variables d'Environnement
Créez un fichier `.env` avec :
```bash
API_FFBB_APP_BEARER_TOKEN=votre_token_ici
MEILISEARCH_BEARER_TOKEN=votre_token_ici
PYTHONPATH=${PWD}/src:${PWD}
PYTHON_PATH=${PWD}/src:${PWD}
```

## 🚀 Scripts Disponibles

### 1. Script de Diagnostic
```bash
./diagnose-ci-issues.sh
```
**Utilisation** : Identifie les problèmes potentiels dans votre environnement
- Vérifie la configuration Python
- Valide les variables d'environnement
- Contrôle la structure du projet
- Teste les imports de base

### 2. Script de CI Complet
```bash
./run-ci-locally.sh
```
**Utilisation** : Réplique exactement le pipeline GitHub Actions
- Pre-commit hooks (formatage, linting)
- Construction du package
- Tests avec le package construit
- Génération des rapports de couverture

## 📝 Étapes Manuelles

Si vous préférez exécuter les étapes une par une :

### 1. Configuration de l'Environnement
```bash
# Charger les variables d'environnement
set -a && source .env && set +a

# Vérifier les variables
echo "Token API: ${API_FFBB_APP_BEARER_TOKEN:0:10}..."
echo "Token Meilisearch: ${MEILISEARCH_BEARER_TOKEN:0:10}..."
```

### 2. Pre-commit Hooks
```bash
# Installer les hooks
pre-commit install

# Exécuter tous les hooks
pre-commit run --all-files --show-diff-on-failure
```

### 3. Construction du Package
```bash
# Nettoyer les builds précédents
tox -e clean

# Construire le package
tox -e build

# Valider le package avec twine
tox -e validate

# Vérifier les artifacts
ls -la dist/
```

### 4. Tests avec le Package
```bash
# Récupérer le nom du wheel
WHEEL_FILE=$(ls dist/*.whl | head -n 1)

# Exécuter les tests avec le package construit
set -a && source .env && set +a && tox --installpkg "$WHEEL_FILE"
```

### 5. Rapport de Couverture
```bash
# Générer les rapports
coverage lcov -o coverage.lcov
coverage html
coverage report

# Ouvrir le rapport HTML
open htmlcov/index.html
```

## 🔍 Commandes de Diagnostic

### Tests Individuels
```bash
# Tester un module spécifique
python -m unittest tests.test_000_api_ffbb_app_client -v

# Tester avec découverte automatique
python -m unittest discover tests -v
```

### Vérification des Hooks
```bash
# Tester un hook spécifique
pre-commit run black --all-files
pre-commit run flake8 --all-files
pre-commit run isort --all-files
```

### Debug du Package
```bash
# Vérifier la version avec setuptools-scm
python -c "from setuptools_scm import get_version; print(get_version())"

# Test d'import
export PYTHONPATH="${PWD}/src:${PWD}"
python -c "import ffbb_data_client; print('Import successful')"
```

## ❌ Problèmes Fréquents et Solutions

### 1. Erreurs de Variables d'Environnement
**Problème** : Tests échouent avec des erreurs d'API
**Solution** :
```bash
# Vérifier que les tokens sont chargés
./diagnose-ci-issues.sh
# Recharger l'environnement si nécessaire
set -a && source .env && set +a
```

### 2. Échec des Pre-commit Hooks
**Problème** : Hooks échouent sur le formatage
**Solution** :
```bash
# Auto-corriger le formatage
black src/ tests/
isort src/ tests/
autoflake --in-place --remove-all-unused-imports --recursive src/ tests/
```

### 3. Erreurs de Construction du Package
**Problème** : setuptools-scm ne trouve pas la version
**Solution** :
```bash
# Vérifier que vous êtes dans un repo git
git status
# Créer un tag si nécessaire
git tag v1.0.0
```

### 4. Tests qui Passent en Local mais Échouent sur CI
**Causes possibles** :
- Différence de version Python (local vs CI)
- Variables d'environnement manquantes dans GitHub Secrets
- Dépendances système différentes

**Solutions** :
1. Utiliser Python 3.11 localement
2. Vérifier les GitHub Secrets
3. Comparer les logs CI avec l'exécution locale

## 📊 Interprétation des Résultats

### ✅ Succès Complet
```
🎉 LOCAL CI PIPELINE COMPLETED SUCCESSFULLY! 🎉
```
Votre code est prêt pour la production !

### ⚠️ Avertissements
- Tests ignorés (skipped) : Normal pour certains tests
- Coverage < 100% : Peut être acceptable selon vos standards

### ❌ Échecs
- Pre-commit : Problèmes de formatage/linting
- Build : Problème de configuration du package
- Tests : Bugs dans le code ou configuration manquante

## 🔗 Ressources Additionnelles

- **Tox Documentation** : https://tox.readthedocs.io/
- **Pre-commit Documentation** : https://pre-commit.com/
- **GitHub Actions** : `.github/workflows/ci.yml`
- **Configuration du Package** : `setup.cfg` et `pyproject.toml`

## 💡 Conseils d'Utilisation

1. **Exécutez toujours le diagnostic en premier** : `./diagnose-ci-issues.sh`
2. **Utilisez le script complet pour la validation finale** : `./run-ci-locally.sh`
3. **Corrigez les problèmes un par un** plutôt qu'en bloc
4. **Committez régulièrement** après avoir corrigé les problèmes
5. **Testez avec des données réelles** (tokens API valides)

---

**Note** : Ces scripts répliquent exactement votre pipeline GitHub Actions. Si quelque chose passe en local mais échoue sur GitHub, vérifiez les variables d'environnement et les versions d'outils.
