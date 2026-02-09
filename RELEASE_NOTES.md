# Release Notes - FFBB API Client V2

## Version 1.2.0 (Next Release)

### 🚀 Major Features & Improvements

#### **Enhanced Token Management System**
- **NEW**: `TokenManager` class for automatic token resolution and centralized management
  - Fetches tokens from environment variables or FFBB API configuration endpoint
  - Uses HTTP-level caching via `CacheManager` for configuration requests
  - `FFBBTokens` dataclass for type-safe token handling
- **IMPROVED**: Simplified authentication workflow - no manual token management required
- **ADDED**: Automatic token validation and error handling

#### **Centralized Configuration Management**
- **NEW**: Centralized configuration module (`config.py`) with all API constants
  - `API_FFBB_BASE_URL`, `MEILISEARCH_BASE_URL` constants
  - `DEFAULT_USER_AGENT` for consistent API requests
  - Endpoint path constants (`ENDPOINT_CONFIGURATION`, `ENDPOINT_LIVES`, etc.)
  - Meilisearch endpoint path constants
- **IMPROVED**: Better maintainability with single source of truth for API URLs

#### **Enhanced Development Experience**
- **NEW**: Parallel test execution with pytest-xdist for faster CI/CD
- **IMPROVED**: Python 3.10 minimum requirement enabling modern language features
- **ADDED**: Comprehensive type annotations throughout the codebase
- **IMPROVED**: MyPy integration with strict type checking

#### **Code Quality & Performance**
- **IMPROVED**: Eliminated all MyPy errors and reduced Pylint warnings significantly
- **ADDED**: MyPy/Pyright configuration and type stubs
- **IMPROVED**: Code formatting and linting standards (Black, Ruff, Flake8)
- **OPTIMIZED**: Reduced test coverage gaps and improved test reliability

### 🔧 Technical Improvements

#### **API Client Architecture**
- **REFACTORED**: Clean separation between API clients and search clients
- **IMPROVED**: Better error handling and logging throughout the codebase
- **ADDED**: Secure logger usage in HTTP helpers (replacing print statements)
- **REFACTORED**: Singleton pattern for CacheManager to prevent multiple instances

#### **Testing Framework Enhancements**
- **BOOSTED**: Test coverage from 81% to 92% with 346 comprehensive tests
- **ADDED**: 51 missing coverage tests and removed 7 dead code functions
- **REFACTORED**: Hierarchical test directory structure for better organization
- **IMPROVED**: Dynamic competition IDs in tests to avoid 403 errors

#### **Model Architecture Refactoring**
- **REFACTORED**: Enforced 1 class = 1 file across all model modules
- **IMPROVED**: Consistent model field types aligned with actual API data
- **MIGRATED**: Models to use new converter_utils helpers (from_str, from_int, etc.)
- **ELIMINATED**: All from_none usage by typing 45 properties across 13 models

### 📚 Documentation & Examples

#### **Enhanced Examples**
- **NEW**: Advanced team ranking analysis example with real-world usage
- **IMPROVED**: Complete usage example with all major features demonstration
- **UPDATED**: Quick start example with modern TokenManager usage
- **ADDED**: Comprehensive example README with usage instructions

#### **Documentation Updates**
- **FIXED**: Critical bugs in README.rst (variable names, package structure)
- **UPDATED**: Migration guide for v1.1.0 and preparation for v1.2.0
- **IMPROVED**: Package structure documentation reflecting current architecture
- **STANDARDIZED**: TokenManager usage examples throughout documentation

### 🐛 Bug Fixes & Stability

- **FIXED**: Model field type mismatches with actual API responses
- **FIXED**: Parsing errors in search results (rencontres, organismes)
- **FIXED**: 403 errors from FFBB API by adding user-agent headers
- **FIXED**: Test flakiness with dynamic competition ID resolution
- **FIXED**: Niveau naming conflicts and dead code removal

### ⚡ Performance Improvements

- **OPTIMIZED**: Parallel test execution reducing CI/CD time
- **IMPROVED**: Efficient model conversion and data parsing
- **ENHANCED**: HTTP caching with CacheManager singleton
- **STREAMLINED**: Codebase with removed dead code and unused imports

### 🔄 Breaking Changes

- **BREAKING**: `TokenManager.get_tokens()` signature changed: `use_cache` parameter replaced by `cache_config`
- **BREAKING**: `TokenManager.clear_cache()` method removed - use `CacheManager().clear()` instead
- **BREAKING**: Python 3.9 support dropped - minimum version now 3.10

**Note**: These changes justify the minor version bump from v1.1.1 to v1.2.0

### 📦 Dependencies

- **UPDATED**: All tools to latest versions (pytest, black, ruff, mypy, etc.)
- **MAINTAINED**: Core dependencies remain compatible
- **IMPROVED**: Better Python 3.10+ compatibility and performance

### 🧪 Testing

- **ADDED**: 51 new test cases covering previously untested code
- **IMPROVED**: Test framework with parallel execution capabilities
- **ENHANCED**: Integration tests with real API validation
- **STABILIZED**: Test suite with dynamic IDs and reduced flakiness

---

## Migration Guide from v1.1.x to v1.2.0

### Token Management Updates
```python
# Before v1.2.0
tokens = TokenManager.get_tokens(use_cache=False)
TokenManager.clear_cache()

# After v1.2.0
tokens = TokenManager.get_tokens(use_cache=False)
from ffbb_api_client_v2.utils.cache_manager import CacheManager
CacheManager().clear()
```

### Python Version Requirement
```bash
# Before: Python 3.9+
# After: Python 3.10+ (minimum)
python3.10 --version
```

---

## Version 1.1.0 (Previous Release)

### 🚀 Major Features & Improvements

#### **Enhanced API Response Models**
- **NEW**: Comprehensive data models with automatic parsing and validation
  - `GetOrganismeResponse` - Complete organization/club data with nested relationships
  - `GetCompetitionResponse` - Competition details with phases, pools, and matches
  - `GetSaisonsResponse` - Season information with active status filtering
  - `GetPouleResponse` - Pool/group data with match details
- **IMPROVED**: All API methods now return strongly-typed model objects instead of raw dictionaries
- **ADDED**: Automatic error handling for invalid API responses and malformed data

#### **Centralized Query Fields Management**
- **NEW**: `QueryFieldsManager` class for consistent field selection across all API methods
- **NEW**: Three field set levels for optimized API calls:
  - `FieldSet.BASIC` - Essential fields only (faster queries)
  - `FieldSet.DEFAULT` - Standard field set (used when fields=None)
  - `FieldSet.DETAILED` - Comprehensive field set with all nested data
- **IMPROVED**: All API methods now use default fields automatically when no fields are specified

#### **Enhanced API Client Methods**
- **IMPROVED**: `get_organisme()` - Now returns `GetOrganismeResponse` with complete club data
  - Includes members, engagements, competitions, venues, and certifications
  - Supports flexible field selection for performance optimization
- **IMPROVED**: `get_competition()` - Enhanced with proper field management and model responses
- **IMPROVED**: `get_saisons()` - Better filtering and list-based responses
- **IMPROVED**: `get_poule()` - Complete pool data with match information
- **NEW**: Automatic API response data extraction from `{"data": {...}}` wrapper format

#### **Better Error Handling & Reliability**
- **IMPROVED**: Robust error handling for API failures and invalid responses
- **ADDED**: Automatic filtering of invalid data items in list responses
- **IMPROVED**: Better handling of missing or null API responses
- **ADDED**: Type safety with proper validation of API response structure

#### **Development & Testing Improvements**
- **NEW**: Comprehensive unittest-based test suite (28 tests) with 100% pass rate
  - Core functionality testing for all client methods
  - Field selection validation
  - Error handling verification
  - Mock-based testing for reliable CI/CD
- **NEW**: Enhanced integration tests with real API validation
  - User journey scenarios testing real-world usage
  - Model validation with actual API responses
  - Performance testing with different field configurations
- **IMPROVED**: Test framework switched from pytest to unittest for better compatibility
- **IMPROVED**: Pre-commit hooks and code quality enforcement
  - Black code formatting
  - Flake8 linting with proper line length limits
  - Import sorting with isort
  - Automated trailing whitespace removal

### 🔧 Technical Improvements

#### **Code Quality & Structure**
- **IMPROVED**: All code now follows strict Python coding standards
- **IMPROVED**: Consistent type hints throughout the codebase
- **IMPROVED**: Better documentation and inline comments
- **ADDED**: Comprehensive flake8 configuration for code quality

#### **Environment & Configuration**
- **IMPROVED**: Environment variable loading with automatic `.env` file support
- **ADDED**: Better configuration examples in documentation
- **IMPROVED**: Token management and validation

### 📚 Documentation Updates

#### **README Enhancements**
- **REWRITTEN**: Complete README with modern features showcase
- **ADDED**: Comprehensive usage examples for all major features
- **ADDED**: Advanced usage patterns with field selection
- **ADDED**: API reference documentation
- **IMPROVED**: Better quick start guide with real examples
- **ADDED**: Environment configuration instructions

#### **Code Examples**
- **ADDED**: Real-world usage scenarios in integration tests
- **ADDED**: Field selection examples for performance optimization
- **ADDED**: Error handling patterns
- **ADDED**: Multi-search functionality examples

### 🐛 Bug Fixes & Stability

- **FIXED**: API response parsing issues with nested data structures
- **FIXED**: Environment variable loading in test environments
- **FIXED**: Field parameter handling in API method calls
- **FIXED**: Pre-commit hook configuration issues
- **FIXED**: Import statements and module organization
- **FIXED**: Test reliability and deterministic behavior

### ⚡ Performance Improvements

- **OPTIMIZED**: API calls with smart field selection
- **IMPROVED**: Request caching for better performance
- **OPTIMIZED**: Data parsing with efficient model conversion
- **REDUCED**: API payload sizes with targeted field queries

### 🔄 Breaking Changes

- **BREAKING**: API methods now return model objects instead of dictionaries
  - Migration: Access data via object attributes instead of dictionary keys
  - Example: `organisme.nom` instead of `organisme['nom']`
- **BREAKING**: Field management now uses centralized `QueryFieldsManager`
  - Migration: Use `QueryFieldsManager.get_*_fields()` for field lists

**Note**: These changes justify the minor version bump from v1.0.1 to v1.1.0

### 📦 Dependencies

- **MAINTAINED**: All existing dependencies remain unchanged
- **ADDED**: Enhanced support for `python-dotenv` for environment management
- **IMPROVED**: Better compatibility with Python 3.11-3.12

### 🧪 Testing

- **ADDED**: 28 comprehensive unittest-based tests covering all functionality
- **ADDED**: Integration tests with real API validation using unittest framework
- **ADDED**: Performance testing with different field configurations
- **IMPROVED**: Test framework migration from pytest to unittest for better compatibility
- **IMPROVED**: Test reliability and CI/CD integration
- **ADDED**: Pre-commit testing to ensure code quality
- **ADDED**: Tox configuration for comprehensive testing across environments

---

## Migration Guide from v1.0.x to v1.1.0

### API Response Objects
```python
# Before v2.1.0
organisme = client.get_organisme(123)
name = organisme['nom']  # Dictionary access

# After v1.1.0
organisme = client.get_organisme(123)
name = organisme.nom  # Object attribute access
```

### Field Selection
```python
# Before v2.1.0
fields = ["id", "nom", "code"]  # Manual field lists

# After v2.1.0
from ffbb_api_client_v2.models.query_fields import QueryFieldsManager, FieldSet
fields = QueryFieldsManager.get_organisme_fields(FieldSet.BASIC)
```

### Error Handling
```python
# After v1.1.0 - Models handle errors automatically
organisme = client.get_organisme(999999)  # Non-existent ID
if organisme is None:
    print("Organization not found")
```

---

## Version 1.0.x (Previous Releases)

Previous releases focused on basic API functionality and package structure. Version 1.1.0 represents a major evolution toward a production-ready, type-safe client library with comprehensive testing and documentation.
