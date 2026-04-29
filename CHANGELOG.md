# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.1] - 2026-04-29

### Changed
- Migrated test suite from `requests` to `httpx` to align with the core project dependencies.

### Fixed
- Fixed bug in `FFBBAPIClientV3.multi_search` that could improperly mutate optional arguments when initialized as `None`.
- Fixed CI formatting errors and resolved Coveralls code coverage report upload issues by correcting `.coveragerc` path omission rules.

## [1.6.0] - 2026-04-24

### Added
- **NEW**: `get_configuration()` / `get_configuration_async()` exposed in `FFBBAPIClientV3` wrapper
- **NEW**: `list_competitions()` / `list_competitions_async()` exposed in `FFBBAPIClientV3` wrapper
- **NEW**: `search_multiple_competitions_async()` exposed in `FFBBAPIClientV3` wrapper
- **NEW**: `search_multiple_organismes_async()` exposed in `FFBBAPIClientV3` wrapper
- **NEW**: `search_multiple_pratiques_async()` exposed in `FFBBAPIClientV3` wrapper
- **NEW**: `search_multiple_salles_async()` exposed in `FFBBAPIClientV3` wrapper
- **NEW**: `search_multiple_terrains_async()` exposed in `FFBBAPIClientV3` wrapper
- **NEW**: `search_multiple_tournois_async()` exposed in `FFBBAPIClientV3` wrapper
- **NEW**: `search_multiple_engagements_async()` exposed in `FFBBAPIClientV3` wrapper
- **NEW**: `search_multiple_formations_async()` exposed in `FFBBAPIClientV3` wrapper
- **NEW**: GitHub Actions workflow `check_wrapper_parity.yml` — automated weekly CI check (every Monday 06:00 UTC) that fails if any public method from inner clients is missing from the wrapper
- **NEW**: `.github/scripts/check_wrapper_parity.py` — AST-based parity script with `@property` exclusion and GitHub Step Summary output

### Fixed
- Wrapper `FFBBAPIClientV3` was silently missing 10 methods previously only accessible via inner clients directly

## [1.5.5] - 2026-04-20

### Added
- **NEW**: SEO-optimized landing page, `sitemap.xml`, `robots.txt` and updated `og:url`
- **NEW**: Added test coverage for `result_from_list` exceptions and `get_classement` delegation

### Changed
- **PERFORMANCE**: Pre-compile regex patterns and optimize SENIOR category deduction in `NiveauExtractor`
- **PERFORMANCE**: Replace O(n²) list operations with O(n) comprehensions in `filter_result` (`MultiSearchQuery`)
- **PERFORMANCE**: Optimize URL parameter encoding and datetime parsing
- Extracted normalization logic from `RencontresHit.__post_init__`
- Rewrote README with PAS framework and content strategy

### Fixed
- Error path in `OrganismesHit.from_dict`
- Trailing whitespace and end-of-file formatting
- CI action failures related to date validation

## [1.5.0] - 2026-04-04

### Added
- **NEW**: `search_engagements` / `search_formations` — two new Meilisearch search methods (sync + async) covering the `ffbbserver_engagements` and `ffbbserver_formations` indexes
- **NEW**: `EngagementsHit`, `FormationsHit`, `FormationSession` models with full field mapping
- **NEW**: `EngagementsMultiSearchQuery`, `FormationsMultiSearchQuery` query classes
- **NEW**: `EngagementsMultiSearchResult`, `FormationsMultiSearchResult` result types
- **NEW**: Facet distribution and stats classes for engagements and formations
- **NEW**: `filter`, `sort`, and `limit` parameters on all `search_*` and `search_multiple_*` methods (Meilisearch native filtering)
- **NEW**: Unit tests for search_engagements, search_formations, filter/sort/limit params (`test_v2_backport_search.py`, `test_123_v2_backport.py`)

### Changed
- `QueryFieldsManager` now inherits from `ABC` with abstract `get_fields()` method
- `FieldSet.BASIC` and `FieldSet.DETAILED` are now aliases for `FieldSet.DEFAULT` (simplified to a single field set)
- `generate_queries()` in `multi_search_query_helper.py` now includes engagements and formations (9 indexes total)

## [1.4.0] - 2026-04-03

### Added
- **NEW**: Sync with upstream v1.4.0 model updates (`organisme_fields`, `team_ranking`, `commune`)

### Improved
- **PERFORMANCE**: Improved async session reuse and HTTP robustness in the main client
- Enhanced data conversion utilities (`converter_utils`) to safely handle edge cases
- Better HTTP fallback logic and session management

### Fixed
- Cherry-picked critical fixes from upstream for Data Models to prevent deserialization errors on null/missing fields
- Type mismatches and formatting edge cases affecting data ingestion

## [1.2.0] - 2025-02-05

### Added
- **NEW**: `TokenManager` class for automatic token resolution
  - Fetches tokens from environment variables or FFBB API
  - Uses HTTP-level caching via `CacheManager` for configuration requests
  - `FFBBTokens` dataclass for type-safe token handling
- **NEW**: Centralized configuration module (`config.py`)
  - `API_FFBB_BASE_URL`, `MEILISEARCH_BASE_URL` constants
  - `DEFAULT_USER_AGENT` constant
  - `ENV_API_TOKEN`, `ENV_MEILISEARCH_TOKEN` environment variable names
  - API endpoint path constants (`ENDPOINT_CONFIGURATION`, `ENDPOINT_LIVES`, etc.)
  - Meilisearch endpoint path constants (`MEILISEARCH_ENDPOINT_MULTI_SEARCH`)
- New tests: `test_019_config.py`, `test_020_token_manager.py`

### Changed
- **BREAKING**: `TokenManager.get_tokens()` signature changed: `use_cache` parameter replaced by `cache_config`
- API clients now use centralized endpoint constants from `config.py`
- Simplified Quick Start examples using TokenManager
- Updated all example scripts to demonstrate TokenManager usage

### Removed
- `TokenManager.clear_cache()` method (use `get_cache_manager().clear()` instead)
- `TokenManager._cached_tokens` class variable (HTTP caching is now used)

### Improved
- No more manual token management required for basic usage
- Environment variable handling is now optional (tokens can be auto-fetched)

## [1.1.1] - 2025-09-16

### Fixed
- Fixed flake8 line length errors that prevented CI workflow from completing
- Updated maximum line length configuration to be compatible with Black formatting
- Improved code formatting consistency across the codebase

## [1.1.0] - 2025-09-16

### Added
- Comprehensive data models with automatic validation (`GetOrganismeResponse`, `GetCompetitionResponse`, `GetSaisonsResponse`, `GetPouleResponse`)
- Centralized query fields management with `QueryFieldsManager` and `FieldSet` enums
- 28 comprehensive unit tests with 100% pass rate
- Enhanced integration tests with real API validation
- Automatic environment variable loading from `.env` files
- Pre-commit hooks for code quality enforcement (Black, Flake8, isort)
- Advanced usage examples in documentation
- API reference documentation
- **NEW**: Team ranking analysis example (`examples/team_ranking_analysis.py`)
- **NEW**: Input validation utilities with secure token handling
- **NEW**: Retry mechanisms with exponential backoff for improved reliability
- **NEW**: Caching system for performance optimization

### Changed
- **BREAKING**: API methods now return strongly-typed model objects instead of dictionaries
- **BREAKING**: Field management now uses centralized `QueryFieldsManager` class
- All API methods use default fields automatically when fields parameter is None
- Improved error handling with automatic invalid data filtering
- Enhanced documentation with comprehensive examples
- Better API response parsing with `{"data": {...}}` wrapper handling
- **SECURITY**: Enhanced secure token logging and validation
- **PERFORMANCE**: Modernized Python code to use Python 3.9+ features (union operators, improved type hints)
- **QUALITY**: Applied comprehensive code formatting (Black, isort, pyupgrade) and linting (flake8)

### Fixed
- API response parsing issues with nested data structures
- Environment variable loading in test environments
- **CLEANUP**: Removed development scripts, temporary files, and redundant documentation
- **CONSISTENCY**: Consolidated CHANGELOG files (removed duplicate .rst version)

### Removed
- Temporary development scripts (`analyze_senas_ranking.py`, `find_pelissanne_*.py`, etc.)
- Cache files and temporary directories (`http_cache/`, `http_cache.db`, etc.)
- Redundant documentation files (Pelissanne analysis docs, duplicate parameters files)
- Duplicate CHANGELOG.rst file in favor of unified CHANGELOG.md

## [1.0.1] - 2025-08-12

### Added
- Basic integration tests and enhanced testing framework
- Improved API client functionality

### Fixed
- Various bug fixes and stability improvements

## [1.0.0.1] - Previous Release

### Added
- Basic FFBB API client functionality
- Search capabilities across multiple resource types
- Request caching support
- Meilisearch integration for search functionality
- Multi-search across all resource types

### Features
- Access to FFBB API endpoints (competitions, organismes, lives, etc.)
- Search functionality for clubs, competitions, matches, venues
- Basic data models and response handling
- PyScaffold-based project structure
- Apache 2.0 licensing

---

## Migration Guide

### From v1.0.x to v1.1.0

**API Response Changes:**
```python
# Before
organisme = client.get_organisme(123)
name = organisme['nom']  # Dictionary access

# After
organisme = client.get_organisme(123)
name = organisme.nom  # Object attribute access
```

**Field Selection:**
```python
# Before
fields = ["id", "nom", "code"]

# After
from ffbb_api_client_v3.models.query_fields import QueryFieldsManager, FieldSet
fields = QueryFieldsManager.get_organisme_fields(FieldSet.BASIC)
```

**Error Handling:**
```python
# After - Automatic error handling
organisme = client.get_organisme(999999)
if organisme is None:
    print("Organization not found or error occurred")
```
