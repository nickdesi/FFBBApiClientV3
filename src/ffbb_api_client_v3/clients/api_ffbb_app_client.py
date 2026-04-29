from __future__ import annotations

from typing import Any

import httpx
from httpx import Client
from pydantic import TypeAdapter

from ..config import (
    API_FFBB_BASE_URL,
    DEFAULT_USER_AGENT,
    ENDPOINT_COMPETITIONS,
    ENDPOINT_CONFIGURATION,
    ENDPOINT_LIVES,
    ENDPOINT_ORGANISMES,
    ENDPOINT_POULES,
    ENDPOINT_SAISONS,
    ENDPOINT_RENCONTRES,
    ENDPOINT_ENGAGEMENTS,
    ENDPOINT_FORMATIONS,
    ENDPOINT_ENTRAINEURS,
    ENDPOINT_COMMUNES,
    ENDPOINT_OFFICIELS,
    ENDPOINT_SALLES,
    ENDPOINT_TERRAINS,
    ENDPOINT_TOURNOIS,
    ENDPOINT_PRATIQUES,
)
from ..helpers.http_requests_helper import catch_result
from ..helpers.http_requests_utils import (
    http_get_json,
    http_get_json_async,
    url_with_params,
)
from ..models.configuration_models import GetConfigurationResponse
from ..models.field_set import FieldSet
from ..models.get_competition_response import GetCompetitionResponse
from ..models.get_organisme_response import GetOrganismeResponse
from ..models.lives import Live
from ..models.poules_models import GetPouleResponse
from ..models.query_fields_manager import QueryFieldsManager
from ..models.saisons_models import GetSaisonsResponse
from ..models.get_rencontre_response import GetRencontreResponse
from ..models.get_engagement_response import GetEngagementResponse
from ..models.get_formation_response import GetFormationResponse
from ..models.get_entraineur_response import GetEntraineurResponse
from ..models.get_commune_response import GetCommuneResponse
from ..models.get_officiel_response import GetOfficielResponse
from ..models.get_salle_response import GetSalleResponse
from ..models.get_terrain_response import GetTerrainResponse
from ..models.get_tournoi_response import GetTournoiResponse
from ..models.get_pratique_response import GetPratiqueResponse
from ..models.team_ranking import TeamRanking
from ..utils.cache_manager import CacheConfig, CacheManager
from ..utils.retry_utils import (
    RetryConfig,
    TimeoutConfig,
    get_default_retry_config,
    get_default_timeout_config,
)
from ..utils.secure_logging import get_secure_logger, mask_token


class ApiFFBBAppClient:
    url: str = ""
    debug: bool = False
    headers: dict[str, str] = {}
    cached_session: Client | None = None
    async_cached_session: httpx.AsyncClient | None = None
    retry_config: RetryConfig | None = None
    timeout_config: TimeoutConfig | None = None

    def __init__(
        self,
        bearer_token: str,
        url: str = API_FFBB_BASE_URL,
        debug: bool = False,
        cached_session: Client | None = None,
        async_cached_session: httpx.AsyncClient | None = None,
        *,
        retry_config: RetryConfig | None = None,
        timeout_config: TimeoutConfig | None = None,
        cache_config: CacheConfig | None = None,
    ):
        """
        Initializes an instance of the ApiFFBBAppClient class.

        Args:
            bearer_token (str): The bearer token used for authentication.
            url (str, optional): The base URL. Defaults to "https://api.ffbb.app/".
            debug (bool, optional): Whether to enable debug mode. Defaults to False.
            cached_session (Client, optional): The cached session to use.
            retry_config (RetryConfig, optional): Retry configuration. Defaults to None.
            timeout_config (TimeoutConfig, optional): Timeout configuration.
                Defaults to None.
            cache_config (CacheConfig, optional): Cache configuration. Defaults to None.
        """
        if not bearer_token or not bearer_token.strip():
            raise ValueError("bearer_token cannot be None, empty, or whitespace-only")

        # Store token securely (private attribute)
        self._bearer_token = bearer_token
        self.url = url
        self.debug = debug
        self.cached_session = cached_session
        self.headers = {
            "Authorization": f"Bearer {self._bearer_token}",
            "user-agent": DEFAULT_USER_AGENT,
        }

        # Configure retry and timeout settings
        self.retry_config = retry_config or get_default_retry_config()
        self.timeout_config = timeout_config or get_default_timeout_config()

        # Configure cache manager
        self.cache_manager = CacheManager(cache_config)

        if cached_session is None:
            self.cached_session = self.cache_manager.session
        else:
            self.cached_session = cached_session

        if async_cached_session is None:
            self.async_cached_session = self.cache_manager.async_session
        else:
            self.async_cached_session = async_cached_session

        # Initialize secure logger
        self.logger = get_secure_logger(f"{self.__class__.__name__}")

        # Log initialization with masked token
        masked_token = mask_token(self._bearer_token)
        if self.debug:
            self.logger.info(f"ApiFFBBAppClient initialized with token: {masked_token}")
            self.logger.info(
                f"Retry config: {self.retry_config.max_attempts} attempts, "
                f"timeout: {self.timeout_config.total_timeout}s"
            )
        else:
            self.logger.info("ApiFFBBAppClient initialized successfully")

    @property
    def bearer_token(self) -> str:
        """Get the bearer token."""
        return self._bearer_token

    def get_lives(self, cached_session: Client | None = None) -> list[Live] | None:
        """
        Retrieves a list of live events with retry logic.

        Args:
            cached_session (Client, optional): The cached session to use

        Returns:
            List[Live]: A list of Live objects representing the live events.
        """
        url = f"{self.url}{ENDPOINT_LIVES}"

        raw_data = catch_result(
            lambda: http_get_json(
                url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
                retry_config=self.retry_config,
                timeout_config=self.timeout_config,
            )
        )
        if raw_data:
            # data might be a list or a dict with "lives" key
            if isinstance(raw_data, dict) and "lives" in raw_data:
                raw_data = raw_data["lives"]

            if not isinstance(raw_data, list):
                return []

            adapter = TypeAdapter(list[Live])
            return adapter.validate_python(raw_data)
        return None

    async def get_lives_async(
        self, cached_session: httpx.AsyncClient | None = None
    ) -> list[Live] | None:
        """
        Retrieves a list of live events asynchroniously.
        """
        url = f"{self.url}{ENDPOINT_LIVES}"

        # Note: catch_result is not async-friendly, but http_get_json_async handles some errors
        # In a real async environment, we might want an async_catch_result
        try:
            raw_data = await http_get_json_async(
                url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.async_cached_session,
                retry_config=self.retry_config,
                timeout_config=self.timeout_config,
            )
            if raw_data is not None:
                # data might be a list or a dict with "lives" key
                if isinstance(raw_data, dict) and "lives" in raw_data:
                    raw_data = raw_data["lives"]

                if not isinstance(raw_data, list):
                    return []

                adapter = TypeAdapter(list[Live])
                return adapter.validate_python(raw_data)
        except Exception as e:
            if self.debug:
                self.logger.error(f"Error in get_lives_async: {e}")
        return None

    def get_competition(
        self,
        competition_id: int,
        deep_limit: str | None = "1000",
        fields: list[str] | None = None,
        cached_session: Client | None = None,
    ) -> GetCompetitionResponse | None:
        """
        Retrieves detailed information about a competition.

        Args:
            competition_id (int): The ID of the competition
            deep_limit (str, optional): Limit for nested rencontres.
                Defaults to "1000".
            fields (List[str], optional): List of fields to retrieve.
                If None, uses default fields.
            cached_session (Client, optional): The cached session to use

        Returns:
            GetCompetitionResponse: Competition data with nested phases,
                poules, and rencontres
        """
        url = f"{self.url}{ENDPOINT_COMPETITIONS}/{competition_id}"

        params: dict[str, Any] = {}
        if deep_limit:
            params["deep[phases][poules][rencontres][_limit]"] = deep_limit

        if fields:
            for field in fields:
                if "fields[]" not in params:
                    params["fields[]"] = []
                params["fields[]"].append(field)
        else:
            # Use default fields from descriptor when no fields are specified
            params["fields[]"] = QueryFieldsManager.get_competition_fields(
                FieldSet.DEFAULT
            )

        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )

        # Extract the actual data from the response wrapper

        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data:
            adapter = TypeAdapter(GetCompetitionResponse)
            return adapter.validate_python(actual_data)
        return None

    async def get_competition_async(
        self,
        competition_id: int,
        deep_limit: str | None = "1000",
        fields: list[str] | None = None,
        cached_session: httpx.AsyncClient | None = None,
    ) -> GetCompetitionResponse | None:
        """
        Retrieves detailed information about a competition asynchroniously.
        """
        url = f"{self.url}{ENDPOINT_COMPETITIONS}/{competition_id}"

        params: dict[str, Any] = {}
        if deep_limit:
            params["deep[phases][poules][rencontres][_limit]"] = deep_limit

        if fields:
            for field in fields:
                if "fields[]" not in params:
                    params["fields[]"] = []
                params["fields[]"].append(field)
        else:
            params["fields[]"] = QueryFieldsManager.get_competition_fields(
                FieldSet.DEFAULT
            )

        final_url = url_with_params(url, params)
        try:
            data = await http_get_json_async(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.async_cached_session,
            )
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            if actual_data:
                adapter = TypeAdapter(GetCompetitionResponse)
                return adapter.validate_python(actual_data)
            return None
        except Exception as e:
            if self.debug:
                self.logger.error(f"Error in get_competition_async: {e}")
            return None

    def get_poule(
        self,
        poule_id: int,
        deep_limit: str | None = "1000",
        fields: list[str] | None = None,
        cached_session: Client | None = None,
    ) -> GetPouleResponse | None:
        """
        Retrieves detailed information about a poule.

        Args:
            poule_id (int): The ID of the poule
            deep_limit (str, optional): Limit for nested rencontres.
                Defaults to "1000".
            fields (List[str], optional): List of fields to retrieve.
                If None, uses default fields.
            cached_session (Client, optional): The cached session to use

        Returns:
            GetPouleResponse: Poule data with rencontres
        """
        url = f"{self.url}{ENDPOINT_POULES}/{poule_id}"

        params: dict[str, Any] = {}
        if deep_limit:
            params["deep[rencontres][_limit]"] = deep_limit
            params["deep[classements][_limit]"] = deep_limit

        if fields:
            params["fields[]"] = fields
        else:
            # Use default fields from descriptor when no fields are specified
            params["fields[]"] = QueryFieldsManager.get_poule_fields(FieldSet.DEFAULT)

        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )

        # Extract the actual data from the response wrapper

        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data:
            return GetPouleResponse.from_dict(actual_data)
        return None

    async def get_poule_async(
        self,
        poule_id: int,
        deep_limit: str | None = "1000",
        fields: list[str] | None = None,
        cached_session: httpx.AsyncClient | None = None,
    ) -> GetPouleResponse | None:
        """
        Retrieves detailed information about a poule asynchroniously.
        """
        url = f"{self.url}{ENDPOINT_POULES}/{poule_id}"

        params: dict[str, Any] = {}
        if deep_limit:
            params["deep[rencontres][_limit]"] = deep_limit
            params["deep[classements][_limit]"] = deep_limit

        if fields:
            params["fields[]"] = fields
        else:
            params["fields[]"] = QueryFieldsManager.get_poule_fields(FieldSet.DEFAULT)

        final_url = url_with_params(url, params)
        try:
            data = await http_get_json_async(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.async_cached_session,
            )
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            if actual_data:
                return GetPouleResponse.from_dict(actual_data)
            return None
        except Exception as e:
            if self.debug:
                self.logger.error(f"Error in get_poule_async: {e}")
            return None

    def get_classement(
        self,
        poule_id: int,
        cached_session: Client | None = None,
    ) -> list[TeamRanking] | None:
        """
        Retrieves ONLY the ranking (classement) for a specific poule.
        """
        res = self.get_poule(
            poule_id=poule_id,
            deep_limit="1000",
            fields=QueryFieldsManager.get_classement_fields(),
            cached_session=cached_session,
        )
        return res.classements if res else None

    async def get_classement_async(
        self,
        poule_id: int,
        cached_session: httpx.AsyncClient | None = None,
    ) -> list[TeamRanking] | None:
        """
        Asynchronously retrieves ONLY the ranking (classement) for a specific poule.
        """
        res = await self.get_poule_async(
            poule_id=poule_id,
            deep_limit="1000",
            fields=QueryFieldsManager.get_classement_fields(),
            cached_session=cached_session,
        )
        return res.classements if res else None

    def get_saisons(
        self,
        fields: list[str] | None = None,
        filter_criteria: str | None = '{"actif":{"_eq":true}}',
        cached_session: Client | None = None,
    ) -> list[GetSaisonsResponse]:
        """
        Retrieves list of seasons.

        Args:
            fields (List[str], optional): List of fields to retrieve.
                If None, uses default fields.
            filter_criteria (str, optional): JSON filter criteria.
                Defaults to active seasons.
            cached_session (Client, optional): The cached session to use

        Returns:
            List[GetSaisonsResponse]: List of season data
        """
        url = f"{self.url}{ENDPOINT_SAISONS}"

        params: dict[str, Any] = {}
        if fields:
            params["fields[]"] = fields
        else:
            # Use default fields from descriptor when no fields are specified
            params["fields[]"] = QueryFieldsManager.get_saison_fields(FieldSet.DEFAULT)

        if filter_criteria:
            params["filter"] = filter_criteria

        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )

        # Extract the actual data from the response wrapper

        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            adapter = TypeAdapter(list[GetSaisonsResponse])
            return adapter.validate_python(actual_data)
        return []

    async def get_saisons_async(
        self,
        fields: list[str] | None = None,
        filter_criteria: str | None = '{"actif":{"_eq":true}}',
        cached_session: httpx.AsyncClient | None = None,
    ) -> list[GetSaisonsResponse]:
        """
        Retrieves list of seasons asynchroniously.
        """
        url = f"{self.url}{ENDPOINT_SAISONS}"

        params: dict[str, Any] = {}
        if fields:
            params["fields[]"] = fields
        else:
            params["fields[]"] = QueryFieldsManager.get_saison_fields(FieldSet.DEFAULT)

        if filter_criteria:
            params["filter"] = filter_criteria

        final_url = url_with_params(url, params)
        try:
            data = await http_get_json_async(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.async_cached_session,
            )
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            if actual_data and isinstance(actual_data, list):
                adapter = TypeAdapter(list[GetSaisonsResponse])
                return adapter.validate_python(actual_data)
        except Exception as e:
            if self.debug:
                self.logger.error(f"Error in get_saisons_async: {e}")
        return []

    def get_organisme(
        self,
        organisme_id: int,
        fields: list[str] | None = None,
        cached_session: Client | None = None,
    ) -> GetOrganismeResponse | None:
        """
        Retrieves detailed information about an organisme.

        Args:
            organisme_id (int): The ID of the organisme
            fields (List[str], optional): List of fields to retrieve.
                If None, uses default fields.
            cached_session (Client, optional): The cached session to use

        Returns:
            GetOrganismeResponse: Organisme data with members, competitions, etc.
        """
        url = f"{self.url}{ENDPOINT_ORGANISMES}/{organisme_id}"

        params: dict[str, Any] = {}
        if fields:
            params["fields[]"] = fields
        else:
            # Use default fields from descriptor when no fields are specified
            params["fields[]"] = QueryFieldsManager.get_organisme_fields(
                FieldSet.DEFAULT
            )

        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )

        # Extract the actual data from the response wrapper

        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data:
            return GetOrganismeResponse.from_dict(actual_data)
        return None

    async def get_organisme_async(
        self,
        organisme_id: int,
        fields: list[str] | None = None,
        cached_session: httpx.AsyncClient | None = None,
    ) -> GetOrganismeResponse | None:
        """
        Retrieves detailed information about an organisme asynchroniously.
        """
        url = f"{self.url}{ENDPOINT_ORGANISMES}/{organisme_id}"

        params: dict[str, Any] = {}
        if fields:
            params["fields[]"] = fields
        else:
            params["fields[]"] = QueryFieldsManager.get_organisme_fields(
                FieldSet.DEFAULT
            )

        final_url = url_with_params(url, params)
        try:
            data = await http_get_json_async(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.async_cached_session,
            )
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            if actual_data:
                return GetOrganismeResponse.from_dict(actual_data)
            return None
        except Exception as e:
            if self.debug:
                self.logger.error(f"Error in get_organisme_async: {e}")
            return None

    def get_equipes(
        self,
        organisme_id: int,
        cached_session: Client | None = None,
    ) -> list[GetOrganismeResponse.EngagementsitemModel] | None:
        """
        Retrieves ONLY the team commitments (engagements) for a specific club.
        """
        res = self.get_organisme(
            organisme_id=organisme_id,
            fields=QueryFieldsManager.get_equipes_fields(),
            cached_session=cached_session,
        )
        return res.engagements if res else None

    async def get_equipes_async(
        self,
        organisme_id: int,
        cached_session: httpx.AsyncClient | None = None,
    ) -> list[GetOrganismeResponse.EngagementsitemModel] | None:
        """
        Asynchronously retrieves ONLY the team commitments (engagements) for a specific club.
        """
        res = await self.get_organisme_async(
            organisme_id=organisme_id,
            fields=QueryFieldsManager.get_equipes_fields(),
            cached_session=cached_session,
        )
        return res.engagements if res else None

    def list_competitions(
        self,
        limit: int = 10,
        fields: list[str] | None = None,
        cached_session: Client | None = None,
    ) -> list[GetCompetitionResponse | None]:
        """
        Lists competitions with optional field selection.

        Args:
            limit (int): Maximum number of competitions to return. Defaults to 10.
            fields (List[str], optional): List of fields to retrieve.
                If None, uses basic fields (id, nom).
            cached_session (Client, optional): The cached session to use

        Returns:
            list[GetCompetitionResponse]: List of competition data
        """
        url = f"{self.url}{ENDPOINT_COMPETITIONS}"

        params: dict[str, Any] = {"limit": str(limit)}

        if fields:
            params["fields[]"] = fields
        else:
            params["fields[]"] = ["id", "nom"]

        final_url = url_with_params(url, params)
        data = catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )

        # Extract the actual data from the response wrapper

        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data and isinstance(actual_data, list):
            adapter = TypeAdapter(list[GetCompetitionResponse])
            return adapter.validate_python(actual_data)
        return []

    async def list_competitions_async(
        self,
        limit: int = 10,
        fields: list[str] | None = None,
        cached_session: httpx.AsyncClient | None = None,
    ) -> list[GetCompetitionResponse | None]:
        """
        Lists competitions with optional field selection asynchroniously.
        """
        url = f"{self.url}{ENDPOINT_COMPETITIONS}"

        params: dict[str, Any] = {"limit": str(limit)}

        if fields:
            params["fields[]"] = fields
        else:
            params["fields[]"] = ["id", "nom"]

        final_url = url_with_params(url, params)
        try:
            data = await http_get_json_async(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.async_cached_session,
            )
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            if actual_data and isinstance(actual_data, list):
                adapter = TypeAdapter(list[GetCompetitionResponse])
                return adapter.validate_python(actual_data)
        except Exception as e:
            if self.debug:
                self.logger.error(f"Error in list_competitions_async: {e}")
        return []

    def get_configuration(
        self,
        cached_session: Client | None = None,
    ) -> GetConfigurationResponse | None:
        """
        Retrieves the API configuration including bearer tokens.

        This endpoint returns configuration data including:
        - key_dh: The API bearer token for api.ffbb.app
        - key_ms: The Meilisearch bearer token for meilisearch-prod.ffbb.app

        Args:
            cached_session (Client, optional): The cached session to use

        Returns:
            GetConfigurationResponse: Configuration data with tokens
        """
        url = f"{self.url}{ENDPOINT_CONFIGURATION}"
        data = catch_result(
            lambda: http_get_json(
                url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
                retry_config=self.retry_config,
                timeout_config=self.timeout_config,
            )
        )

        # Extract the actual data from the response wrapper

        actual_data = data.get("data") if data and isinstance(data, dict) else data
        if actual_data:
            adapter = TypeAdapter(GetConfigurationResponse)
            return adapter.validate_python(actual_data)
        return None

    async def get_configuration_async(
        self,
        cached_session: httpx.AsyncClient | None = None,
    ) -> GetConfigurationResponse | None:
        """
        Retrieves the API configuration including bearer tokens asynchroniously.
        """
        url = f"{self.url}{ENDPOINT_CONFIGURATION}"
        try:
            data = await http_get_json_async(
                url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.async_cached_session,
                retry_config=self.retry_config,
                timeout_config=self.timeout_config,
            )
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            if actual_data:
                adapter = TypeAdapter(GetConfigurationResponse)
                return adapter.validate_python(actual_data)
            return None
        except Exception as e:
            if self.debug:
                self.logger.error(f"Error in get_configuration_async: {e}")
            return None

    def get_rencontre(self, id: str, cached_session: Client | None = None) -> GetRencontreResponse | None:
        """Retrieves detailed information about a rencontre."""
        url = f"{self.url}{ENDPOINT_RENCONTRES}/{id}"
        data = catch_result(lambda: http_get_json(url, self.headers, debug=self.debug, cached_session=cached_session or self.cached_session))
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetRencontreResponse.from_dict(actual_data) if actual_data else None

    async def get_rencontre_async(self, id: str, cached_session: httpx.AsyncClient | None = None) -> GetRencontreResponse | None:
        """Asynchronously retrieves detailed information about a rencontre."""
        url = f"{self.url}{ENDPOINT_RENCONTRES}/{id}"
        try:
            data = await http_get_json_async(url, self.headers, debug=self.debug, cached_session=cached_session or self.async_cached_session)
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            return GetRencontreResponse.from_dict(actual_data) if actual_data else None
        except Exception as e:
            if self.debug: self.logger.error(f"Error in get_rencontre_async: {e}")
            return None

    def get_engagement(self, id: str, cached_session: Client | None = None) -> GetEngagementResponse | None:
        """Retrieves detailed information about an engagement."""
        url = f"{self.url}{ENDPOINT_ENGAGEMENTS}/{id}"
        data = catch_result(lambda: http_get_json(url, self.headers, debug=self.debug, cached_session=cached_session or self.cached_session))
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetEngagementResponse.from_dict(actual_data) if actual_data else None

    async def get_engagement_async(self, id: str, cached_session: httpx.AsyncClient | None = None) -> GetEngagementResponse | None:
        """Asynchronously retrieves detailed information about an engagement."""
        url = f"{self.url}{ENDPOINT_ENGAGEMENTS}/{id}"
        try:
            data = await http_get_json_async(url, self.headers, debug=self.debug, cached_session=cached_session or self.async_cached_session)
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            return GetEngagementResponse.from_dict(actual_data) if actual_data else None
        except Exception as e:
            if self.debug: self.logger.error(f"Error in get_engagement_async: {e}")
            return None

    def get_formation(self, id: str, cached_session: Client | None = None) -> GetFormationResponse | None:
        """Retrieves detailed information about a formation."""
        url = f"{self.url}{ENDPOINT_FORMATIONS}/{id}"
        data = catch_result(lambda: http_get_json(url, self.headers, debug=self.debug, cached_session=cached_session or self.cached_session))
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetFormationResponse.from_dict(actual_data) if actual_data else None

    async def get_formation_async(self, id: str, cached_session: httpx.AsyncClient | None = None) -> GetFormationResponse | None:
        """Asynchronously retrieves detailed information about a formation."""
        url = f"{self.url}{ENDPOINT_FORMATIONS}/{id}"
        try:
            data = await http_get_json_async(url, self.headers, debug=self.debug, cached_session=cached_session or self.async_cached_session)
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            return GetFormationResponse.from_dict(actual_data) if actual_data else None
        except Exception as e:
            if self.debug: self.logger.error(f"Error in get_formation_async: {e}")
            return None

    def get_entraineur(self, id: str, cached_session: Client | None = None) -> GetEntraineurResponse | None:
        """Retrieves detailed information about an entraineur."""
        url = f"{self.url}{ENDPOINT_ENTRAINEURS}/{id}"
        data = catch_result(lambda: http_get_json(url, self.headers, debug=self.debug, cached_session=cached_session or self.cached_session))
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetEntraineurResponse.from_dict(actual_data) if actual_data else None

    async def get_entraineur_async(self, id: str, cached_session: httpx.AsyncClient | None = None) -> GetEntraineurResponse | None:
        """Asynchronously retrieves detailed information about an entraineur."""
        url = f"{self.url}{ENDPOINT_ENTRAINEURS}/{id}"
        try:
            data = await http_get_json_async(url, self.headers, debug=self.debug, cached_session=cached_session or self.async_cached_session)
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            return GetEntraineurResponse.from_dict(actual_data) if actual_data else None
        except Exception as e:
            if self.debug: self.logger.error(f"Error in get_entraineur_async: {e}")
            return None

    def get_commune(self, id: str, cached_session: Client | None = None) -> GetCommuneResponse | None:
        """Retrieves detailed information about a commune."""
        url = f"{self.url}{ENDPOINT_COMMUNES}/{id}"
        data = catch_result(lambda: http_get_json(url, self.headers, debug=self.debug, cached_session=cached_session or self.cached_session))
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetCommuneResponse.from_dict(actual_data) if actual_data else None

    async def get_commune_async(self, id: str, cached_session: httpx.AsyncClient | None = None) -> GetCommuneResponse | None:
        """Asynchronously retrieves detailed information about a commune."""
        url = f"{self.url}{ENDPOINT_COMMUNES}/{id}"
        try:
            data = await http_get_json_async(url, self.headers, debug=self.debug, cached_session=cached_session or self.async_cached_session)
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            return GetCommuneResponse.from_dict(actual_data) if actual_data else None
        except Exception as e:
            if self.debug: self.logger.error(f"Error in get_commune_async: {e}")
            return None

    def get_officiel(self, id: str, cached_session: Client | None = None) -> GetOfficielResponse | None:
        """Retrieves detailed information about an officiel."""
        url = f"{self.url}{ENDPOINT_OFFICIELS}/{id}"
        data = catch_result(lambda: http_get_json(url, self.headers, debug=self.debug, cached_session=cached_session or self.cached_session))
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetOfficielResponse.from_dict(actual_data) if actual_data else None

    async def get_officiel_async(self, id: str, cached_session: httpx.AsyncClient | None = None) -> GetOfficielResponse | None:
        """Asynchronously retrieves detailed information about an officiel."""
        url = f"{self.url}{ENDPOINT_OFFICIELS}/{id}"
        try:
            data = await http_get_json_async(url, self.headers, debug=self.debug, cached_session=cached_session or self.async_cached_session)
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            return GetOfficielResponse.from_dict(actual_data) if actual_data else None
        except Exception as e:
            if self.debug: self.logger.error(f"Error in get_officiel_async: {e}")
            return None

    def get_salle(self, id: str, cached_session: Client | None = None) -> GetSalleResponse | None:
        """Retrieves detailed information about a salle."""
        url = f"{self.url}{ENDPOINT_SALLES}/{id}"
        data = catch_result(lambda: http_get_json(url, self.headers, debug=self.debug, cached_session=cached_session or self.cached_session))
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetSalleResponse.from_dict(actual_data) if actual_data else None

    async def get_salle_async(self, id: str, cached_session: httpx.AsyncClient | None = None) -> GetSalleResponse | None:
        """Asynchronously retrieves detailed information about a salle."""
        url = f"{self.url}{ENDPOINT_SALLES}/{id}"
        try:
            data = await http_get_json_async(url, self.headers, debug=self.debug, cached_session=cached_session or self.async_cached_session)
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            return GetSalleResponse.from_dict(actual_data) if actual_data else None
        except Exception as e:
            if self.debug: self.logger.error(f"Error in get_salle_async: {e}")
            return None

    def get_terrain(self, id: str, cached_session: Client | None = None) -> GetTerrainResponse | None:
        """Retrieves detailed information about a terrain."""
        url = f"{self.url}{ENDPOINT_TERRAINS}/{id}"
        data = catch_result(lambda: http_get_json(url, self.headers, debug=self.debug, cached_session=cached_session or self.cached_session))
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetTerrainResponse.from_dict(actual_data) if actual_data else None

    async def get_terrain_async(self, id: str, cached_session: httpx.AsyncClient | None = None) -> GetTerrainResponse | None:
        """Asynchronously retrieves detailed information about a terrain."""
        url = f"{self.url}{ENDPOINT_TERRAINS}/{id}"
        try:
            data = await http_get_json_async(url, self.headers, debug=self.debug, cached_session=cached_session or self.async_cached_session)
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            return GetTerrainResponse.from_dict(actual_data) if actual_data else None
        except Exception as e:
            if self.debug: self.logger.error(f"Error in get_terrain_async: {e}")
            return None

    def get_tournoi(self, id: str, cached_session: Client | None = None) -> GetTournoiResponse | None:
        """Retrieves detailed information about a tournoi."""
        url = f"{self.url}{ENDPOINT_TOURNOIS}/{id}"
        data = catch_result(lambda: http_get_json(url, self.headers, debug=self.debug, cached_session=cached_session or self.cached_session))
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetTournoiResponse.from_dict(actual_data) if actual_data else None

    async def get_tournoi_async(self, id: str, cached_session: httpx.AsyncClient | None = None) -> GetTournoiResponse | None:
        """Asynchronously retrieves detailed information about a tournoi."""
        url = f"{self.url}{ENDPOINT_TOURNOIS}/{id}"
        try:
            data = await http_get_json_async(url, self.headers, debug=self.debug, cached_session=cached_session or self.async_cached_session)
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            return GetTournoiResponse.from_dict(actual_data) if actual_data else None
        except Exception as e:
            if self.debug: self.logger.error(f"Error in get_tournoi_async: {e}")
            return None

    def get_pratique(self, id: str, cached_session: Client | None = None) -> GetPratiqueResponse | None:
        """Retrieves detailed information about a pratique."""
        url = f"{self.url}{ENDPOINT_PRATIQUES}/{id}"
        data = catch_result(lambda: http_get_json(url, self.headers, debug=self.debug, cached_session=cached_session or self.cached_session))
        actual_data = data.get("data") if data and isinstance(data, dict) else data
        return GetPratiqueResponse.from_dict(actual_data) if actual_data else None

    async def get_pratique_async(self, id: str, cached_session: httpx.AsyncClient | None = None) -> GetPratiqueResponse | None:
        """Asynchronously retrieves detailed information about a pratique."""
        url = f"{self.url}{ENDPOINT_PRATIQUES}/{id}"
        try:
            data = await http_get_json_async(url, self.headers, debug=self.debug, cached_session=cached_session or self.async_cached_session)
            actual_data = data.get("data") if data and isinstance(data, dict) else data
            return GetPratiqueResponse.from_dict(actual_data) if actual_data else None
        except Exception as e:
            if self.debug: self.logger.error(f"Error in get_pratique_async: {e}")
            return None
