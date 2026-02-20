from __future__ import annotations

from typing import cast

from httpx import Client

from ..helpers.multi_search_query_helper import generate_queries
from ..models.competitions_multi_search_query import CompetitionsMultiSearchQuery
from ..models.get_competition_response import GetCompetitionResponse
from ..models.get_organisme_response import GetOrganismeResponse
from ..models.lives import Live
from ..models.multi_search_result_competitions import CompetitionsMultiSearchResult
from ..models.multi_search_result_organismes import OrganismesMultiSearchResult
from ..models.multi_search_result_pratiques import PratiquesMultiSearchResult
from ..models.multi_search_result_rencontres import RencontresMultiSearchResult
from ..models.multi_search_result_salles import SallesMultiSearchResult
from ..models.multi_search_result_terrains import TerrainsMultiSearchResult
from ..models.multi_search_result_tournois import TournoisMultiSearchResult
from ..models.multi_search_results import MultiSearchResult
from ..models.organismes_multi_search_query import OrganismesMultiSearchQuery
from ..models.poules_models import GetPouleResponse
from ..models.pratiques_multi_search_query import PratiquesMultiSearchQuery
from ..models.rencontres_multi_search_query import RencontresMultiSearchQuery
from ..models.saisons_models import GetSaisonsResponse
from ..models.salles_multi_search_query import SallesMultiSearchQuery
from ..models.terrains_multi_search_query import TerrainsMultiSearchQuery
from ..models.tournois_multi_search_query import TournoisMultiSearchQuery
from ..utils.cache_manager import CacheManager
from ..utils.input_validation import (
    validate_boolean,
    validate_filter_criteria,
    validate_search_query,
    validate_string_list,
    validate_token,
)
from .api_ffbb_app_client import ApiFFBBAppClient
from .meilisearch_ffbb_client import MeilisearchFFBBClient


class FFBBAPIClientV2:
    def __init__(
        self,
        api_ffbb_client: ApiFFBBAppClient,
        meilisearch_ffbb_client: MeilisearchFFBBClient,
    ):
        self.api_ffbb_client = api_ffbb_client
        self.meilisearch_ffbb_client = meilisearch_ffbb_client

    @staticmethod
    def create(
        meilisearch_bearer_token: str,
        api_bearer_token: str,
        debug: bool = False,
        cached_session: Client | None = None,
    ) -> FFBBAPIClientV2:
        """
        Create a new FFBB API Client V2 instance with comprehensive input validation.

        Args:
            meilisearch_bearer_token (str): Bearer token for Meilisearch API
            api_bearer_token (str): Bearer token for FFBB API
            debug (bool, optional): Enable debug logging. Defaults to False.
            cached_session (Client, optional): HTTP cache session

        Returns:
            FFBBAPIClientV2: Configured API client instance

        Raises:
            ValidationError: If any input parameter is invalid
        """
        # Validate inputs with comprehensive checks
        validated_meilisearch_token = validate_token(
            meilisearch_bearer_token, "meilisearch_bearer_token"
        )
        validated_api_token = validate_token(api_bearer_token, "api_bearer_token")
        validated_debug = validate_boolean(debug, "debug")

        # Use singleton session if not provided
        if cached_session is None:
            cached_session = CacheManager().session

        # Create API clients with validated parameters
        api_ffbb_client = ApiFFBBAppClient(
            validated_api_token, debug=validated_debug, cached_session=cached_session
        )

        meilisearch_ffbb_client: MeilisearchFFBBClient = MeilisearchFFBBClient(
            validated_meilisearch_token,
            debug=validated_debug,
            cached_session=cached_session,
        )

        return FFBBAPIClientV2(api_ffbb_client, meilisearch_ffbb_client)

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
            fields (List[str], optional): List of fields to retrieve
            cached_session (Client, optional): The cached session to use

        Returns:
            GetCompetitionResponse: Competition data with nested phases,
                poules, and rencontres
        """
        return self.api_ffbb_client.get_competition(
            competition_id=competition_id,
            deep_limit=deep_limit,
            fields=fields,
            cached_session=cached_session,
        )

    def get_lives(
        self, cached_session: Client | None = None
    ) -> list[Live] | None:
        """
        Retrieves a list of live events.

        Args:
            cached_session (Client, optional): The cached session to use

        Returns:
            list[Live]: A list of Live objects representing the live events.
        """
        return self.api_ffbb_client.get_lives(cached_session)

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
            fields (List[str], optional): List of fields to retrieve
            cached_session (Client, optional): The cached session to use

        Returns:
            GetOrganismeResponse: Organisme data with members, competitions, etc.
        """
        return self.api_ffbb_client.get_organisme(
            organisme_id=organisme_id,
            fields=fields,
            cached_session=cached_session,
        )

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
            fields (List[str], optional): List of fields to retrieve
            cached_session (Client, optional): The cached session to use

        Returns:
            GetPouleResponse: Poule data with rencontres
        """
        return self.api_ffbb_client.get_poule(
            poule_id=poule_id,
            deep_limit=deep_limit,
            fields=fields,
            cached_session=cached_session,
        )

    def get_saisons(
        self,
        fields: list[str] | None = None,
        filter_criteria: str | None = '{"actif":{"_eq":true}}',
        cached_session: Client | None = None,
    ) -> list[GetSaisonsResponse] | None:
        """
        Retrieves list of seasons with comprehensive input validation.

        Args:
            fields (List[str], optional): List of fields to retrieve.
                 Defaults to ["id"].
            filter_criteria (str, optional): JSON filter criteria.
                 Defaults to active seasons.
            cached_session (Client, optional): The cached session to use

        Returns:
            List[GetSaisonsResponse]: List of season data

        Raises:
            ValidationError: If input parameters are invalid
        """
        validated_fields = validate_string_list(fields, "fields")
        validated_filter = validate_filter_criteria(filter_criteria, "filter_criteria")

        return self.api_ffbb_client.get_saisons(
            fields=validated_fields,
            filter_criteria=validated_filter,
            cached_session=cached_session,
        )

    async def get_lives_async(self) -> list[Live] | None:
        """Retrieves a list of live events asynchronously."""
        return await self.api_ffbb_client.get_lives_async()

    async def get_saisons_async(
        self, active_only: bool = True
    ) -> list[GetSaisonsResponse]:
        """Retrieves list of seasons asynchronously."""
        filter_criteria = '{"actif":{"_eq":true}}' if active_only else None
        return await self.api_ffbb_client.get_saisons_async(filter_criteria=filter_criteria)

    async def get_competition_async(
        self,
        competition_id: int,
        deep_limit: str | None = "1000",
    ) -> GetCompetitionResponse | None:
        """Retrieves detailed information about a competition asynchronously."""
        return await self.api_ffbb_client.get_competition_async(
            competition_id, deep_limit=deep_limit
        )

    async def get_organisme_async(self, organisme_id: int) -> GetOrganismeResponse | None:
        """Retrieves detailed information about an organisme asynchronously."""
        return await self.api_ffbb_client.get_organisme_async(organisme_id)

    async def get_poule_async(
        self, poule_id: int, deep_limit: str | None = "1000"
    ) -> GetPouleResponse | None:
        """Retrieves detailed information about a poule asynchronously."""
        return await self.api_ffbb_client.get_poule_async(poule_id, deep_limit=deep_limit)

    async def multi_search_async(
        self, queries: Sequence[MultiSearchQuery] | None = None
    ) -> MultiSearchResults | None:
        """Performs a smart multi-search asynchronously."""
        return await self.meilisearch_ffbb_client.recursive_smart_multi_search_async(queries)

    def multi_search(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> list[MultiSearchResult] | None:
        """
        Perform multi-search across all resource types with input validation.

        Args:
            name (str, optional): Search query string
            cached_session (Client, optional): HTTP cache session

        Returns:
            list[MultiSearchResult]: Search results across all resource types

        Raises:
            ValidationError: If search query is invalid
        """
        validated_name = validate_search_query(name, "name")
        queries = generate_queries(validated_name)
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session=cached_session
        )

        return results.results if results else None

    def search_competitions(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> CompetitionsMultiSearchResult | None:
        results = self.search_multiple_competitions([name], cached_session)
        return results[0] if results else None

    def search_multiple_competitions(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[CompetitionsMultiSearchResult] | None:
        if not names:
            return None

        queries = [CompetitionsMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[CompetitionsMultiSearchResult], results.results)
            if results
            else None
        )

    def search_multiple_organismes(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[OrganismesMultiSearchResult] | None:
        if not names:
            return None

        queries = [OrganismesMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[OrganismesMultiSearchResult], results.results)
            if results
            else None
        )

    def search_multiple_pratiques(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[PratiquesMultiSearchResult] | None:
        if not names:
            return None

        queries = [PratiquesMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[PratiquesMultiSearchResult], results.results) if results else None
        )

    def search_multiple_rencontres(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[RencontresMultiSearchResult] | None:
        if not names:
            return None

        queries = [RencontresMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[RencontresMultiSearchResult], results.results)
            if results
            else None
        )

    def search_multiple_salles(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[SallesMultiSearchResult] | None:
        if not names:
            return None

        queries = [SallesMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return cast(list[SallesMultiSearchResult], results.results) if results else None

    def search_multiple_terrains(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[TerrainsMultiSearchResult] | None:
        if not names:
            return None

        queries = [TerrainsMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[TerrainsMultiSearchResult], results.results) if results else None
        )

    def search_multiple_tournois(
        self,
        names: list[str | None] | None = None,
        cached_session: Client | None = None,
    ) -> list[TournoisMultiSearchResult] | None:
        if not names:
            return None

        queries = [TournoisMultiSearchQuery(name) for name in names]
        results = self.meilisearch_ffbb_client.recursive_smart_multi_search(
            queries, cached_session
        )

        return (
            cast(list[TournoisMultiSearchResult], results.results) if results else None
        )

    def search_organismes(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> OrganismesMultiSearchResult | None:
        results = self.search_multiple_organismes([name], cached_session)
        return results[0] if results else None

    def search_pratiques(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> PratiquesMultiSearchResult | None:
        results = self.search_multiple_pratiques([name], cached_session)
        return results[0] if results else None

    def search_rencontres(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> RencontresMultiSearchResult | None:
        results = self.search_multiple_rencontres([name], cached_session)
        return results[0] if results else None

    def search_salles(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> SallesMultiSearchResult | None:
        results = self.search_multiple_salles([name], cached_session)
        return results[0] if results else None

    def search_terrains(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> TerrainsMultiSearchResult | None:
        results = self.search_multiple_terrains([name], cached_session)
        return results[0] if results else None

    def search_tournois(
        self, name: str | None = None, cached_session: Client | None = None
    ) -> TournoisMultiSearchResult | None:
        results = self.search_multiple_tournois([name], cached_session)
        return results[0] if results else None

    async def search_competitions_async(
        self, name: str | None = None
    ) -> CompetitionsMultiSearchResult | None:
        """Search for competitions asynchronously."""
        if not name:
            return None
        queries = [CompetitionsMultiSearchQuery(name)]
        results = await self.meilisearch_ffbb_client.recursive_smart_multi_search_async(queries)
        return cast(CompetitionsMultiSearchResult, results.results[0]) if results and results.results else None

    async def search_organismes_async(
        self, name: str | None = None
    ) -> OrganismesMultiSearchResult | None:
        """Search for organismes asynchronously."""
        if not name:
            return None
        queries = [OrganismesMultiSearchQuery(name)]
        results = await self.meilisearch_ffbb_client.recursive_smart_multi_search_async(queries)
        return cast(OrganismesMultiSearchResult, results.results[0]) if results and results.results else None

    async def search_rencontres_async(
        self, name: str | None = None
    ) -> RencontresMultiSearchResult | None:
        """Search for rencontres asynchronously."""
        if not name:
            return None
        queries = [RencontresMultiSearchQuery(name)]
        results = await self.meilisearch_ffbb_client.recursive_smart_multi_search_async(queries)
        return cast(RencontresMultiSearchResult, results.results[0]) if results and results.results else None

    async def search_salles_async(
        self, name: str | None = None
    ) -> SallesMultiSearchResult | None:
        """Search for salles asynchronously."""
        if not name:
            return None
        queries = [SallesMultiSearchQuery(name)]
        results = await self.meilisearch_ffbb_client.recursive_smart_multi_search_async(queries)
        return cast(SallesMultiSearchResult, results.results[0]) if results and results.results else None

    async def search_tournois_async(
        self, name: str | None = None
    ) -> TournoisMultiSearchResult | None:
        """Search for tournois asynchronously."""
        if not name:
            return None
        queries = [TournoisMultiSearchQuery(name)]
        results = await self.meilisearch_ffbb_client.recursive_smart_multi_search_async(queries)
        return cast(TournoisMultiSearchResult, results.results[0]) if results and results.results else None

    async def search_terrains_async(
        self, name: str | None = None
    ) -> TerrainsMultiSearchResult | None:
        """Search for terrains asynchronously."""
        if not name:
            return None
        queries = [TerrainsMultiSearchQuery(name)]
        results = await self.meilisearch_ffbb_client.recursive_smart_multi_search_async(queries)
        return cast(TerrainsMultiSearchResult, results.results[0]) if results and results.results else None

    async def search_pratiques_async(
        self, name: str | None = None
    ) -> PratiquesMultiSearchResult | None:
        """Search for pratiques asynchronously."""
        if not name:
            return None
        queries = [PratiquesMultiSearchQuery(name)]
        results = await self.meilisearch_ffbb_client.recursive_smart_multi_search_async(queries)
        return cast(PratiquesMultiSearchResult, results.results[0]) if results and results.results else None
