#!/usr/bin/env python3
"""
Complete usage example for FFBB API Client V2

This example demonstrates all major features of the FFBB API Client V2,
including model-based responses, field selection, and error handling.

Prerequisites:
- (Optional) Set up your .env file with API tokens for manual configuration
"""

from ffbb_data_client import FFBBDataClient, TokenManager
from ffbb_data_client.models.field_set import FieldSet
from ffbb_data_client.models.query_fields_manager import QueryFieldsManager


def main():
    """Main example function demonstrating FFBB API Client V2 usage with comprehensive error handling."""

    print("🚀 Initializing FFBB API Client V2...")
    print("=" * 60)

    try:
        # Method 1: Automatic token management (Recommended)
        print("🔑 Using TokenManager for automatic token retrieval...")
        tokens = TokenManager.get_tokens()

        client = FFBBDataClient.create(
            api_bearer_token=tokens.api_token,
            meilisearch_bearer_token=tokens.meilisearch_token,
        )

        print("✅ Client initialized successfully!\n")

    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        print("💡 Check your environment configuration")
        return

    # Alternative Method: Manual token management (if needed)
    # import os
    # from dotenv import load_dotenv
    # load_dotenv()
    # api_token = os.getenv("API_FFBB_APP_BEARER_TOKEN")
    # meilisearch_token = os.getenv("MEILISEARCH_BEARER_TOKEN")
    # client = FFBBDataClient.create(
    #     api_bearer_token=api_token, meilisearch_bearer_token=meilisearch_token
    # )

    # Example 1: Search for organizations
    print("=" * 60)
    print("EXAMPLE 1: SEARCHING FOR ORGANIZATIONS")
    print("=" * 60)

    city = "Paris"
    print(f"🔍 Searching for basketball organizations in {city}...")

    organisations_result = client.search_organismes(city)
    print(f"✅ Found {len(organisations_result.hits)} organizations")

    if organisations_result.hits:
        # Get the first organization
        first_org = organisations_result.hits[0]
        print(f"\n📍 First organization: {first_org.nom}")
        print(f"   ID: {first_org.id}")
        print(f"   Type: {first_org.type or 'N/A'}")

        # Example 2: Get detailed organization information with different field sets
        print("\n" + "=" * 60)
        print("EXAMPLE 2: ORGANIZATION DETAILS WITH FIELD SELECTION")
        print("=" * 60)

        org_id = int(first_org.id)

        # Get with basic fields
        print(f"📋 Getting organization {org_id} with BASIC fields...")
        basic_fields = QueryFieldsManager.get_organisme_fields(FieldSet.BASIC)
        org_basic = client.get_organisme(org_id, fields=basic_fields)

        if org_basic:
            print(f"✅ Basic info: {org_basic.nom}")
            print(f"   Code: {org_basic.code}")
            print(f"   Address: {org_basic.adresse}")

        # Get with default fields (automatically selected)
        print(f"\n📋 Getting organization {org_id} with DEFAULT fields...")
        org_default = client.get_organisme(org_id)  # No fields specified = default

        if org_default:
            print(f"✅ Default info: {org_default.nom}")
            print(f"   Type: {org_default.type}")
            print(f"   Email: {org_default.mail}")
            print(
                f"   Teams: "
                f"{len(org_default.engagements) if org_default.engagements else 0}"
            )

            if org_default.commune:
                print(
                    f"   City: {org_default.commune.libelle} "
                    f"({org_default.commune.codePostal})"
                )

        # Get with detailed fields
        print(f"\n📋 Getting organization {org_id} with DETAILED fields...")
        org_detailed = client.get_organisme(org_id)

        if org_detailed:
            print(f"✅ Detailed info: {org_detailed.nom}")
            print(
                f"   Members: "
                f"{len(org_detailed.membres) if org_detailed.membres else 0}"
            )
            print(
                f"   Teams: "
                f"{len(org_detailed.engagements) if org_detailed.engagements else 0}"
            )
            print(
                f"   Competitions: "
                f"{len(org_detailed.competitions) if org_detailed.competitions else 0}"
            )

            if org_detailed.engagements:
                print(f"   First team: {org_detailed.engagements[0].id}")
                if org_detailed.engagements[0].idCompetition:
                    comp = org_detailed.engagements[0].idCompetition
                    print(f"     -> Competition: {comp.nom} ({comp.id})")

    # Example 3: Get current seasons
    print("\n" + "=" * 60)
    print("EXAMPLE 3: CURRENT SEASONS")
    print("=" * 60)

    print("📅 Getting current seasons...")
    seasons = client.get_saisons()

    if seasons:
        print(f"✅ Found {len(seasons)} seasons")
        for season in seasons[:3]:  # Show first 3 seasons
            status = "Active" if season.actif else "Inactive"
            print(f"   • {season.nom} (ID: {season.id}) - {status}")

    # Example 4: Live matches
    print("\n" + "=" * 60)
    print("EXAMPLE 4: LIVE MATCHES")
    print("=" * 60)

    print("⚡ Getting live matches...")
    lives = client.get_lives()

    if lives:
        print(f"Found {len(lives)} live matches")
        for live in lives[:3]:  # Show first 3 live matches
            print(f"   {live.team_name_home} vs {live.team_name_out}")
    else:
        print("ℹ️  No live matches at the moment")

    # Example 5: Multi-search functionality
    print("\n" + "=" * 60)
    print("EXAMPLE 5: MULTI-SEARCH ACROSS ALL RESOURCES")
    print("=" * 60)

    search_term = "Lyon"
    print(f"🔍 Multi-search for '{search_term}' across all resource types...")

    multi_results = client.multi_search(search_term)

    if multi_results:
        print(f"✅ Found results across {len(multi_results)} different resource types")
        for result in multi_results:
            result_type = type(result).__name__.replace("MultiSearchResult", "")
            print(f"   📊 {result_type}: {len(result.hits)} results")

            # Show first result from each category
            if result.hits:
                first_hit = result.hits[0]
                print(f"      -> ID: {first_hit.id}")

    # Example 6: Error handling
    print("\n" + "=" * 60)
    print("EXAMPLE 6: ERROR HANDLING")
    print("=" * 60)

    print("🧪 Testing error handling with non-existent organization...")
    invalid_org = client.get_organisme(999999999)

    if invalid_org is None:
        print("✅ Error handling works correctly - returned None for invalid ID")
    else:
        print("⚠️  Unexpected: got result for invalid ID")

    # Example 7: Competition details
    print("\n" + "=" * 60)
    print("EXAMPLE 7: COMPETITION DETAILS")
    print("=" * 60)

    # Search for competitions first
    comp_results = client.search_competitions("Championnat")

    if comp_results and comp_results.hits:
        print(f"🏆 Found {len(comp_results.hits)} competitions")
        first_comp = comp_results.hits[0]
        comp_id = int(first_comp.id)

        print(f"📋 Getting details for competition: {first_comp.nom}")
        competition = client.get_competition(comp_id)

        if competition:
            print(f"✅ Competition: {competition.nom}")
            print(f"   Season: {competition.saison}")
            print(f"   Type: {competition.typeCompetition}")
            print(f"   Gender: {competition.sexe}")
            print(f"   Live Stats: {'Yes' if competition.liveStat else 'No'}")

    print("\n" + "=" * 60)
    print("🎉 EXAMPLE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n✨ The FFBB API Client V2 provides:")
    print("   • Type-safe model objects for all API responses")
    print("   • Flexible field selection for optimized queries")
    print("   • Comprehensive error handling")
    print("   • Multi-search across all resource types")
    print("   • Easy-to-use interface with detailed examples")
    print("\n📚 Check out the test files for more usage examples!")


if __name__ == "__main__":
    main()
