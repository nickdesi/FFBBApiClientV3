#!/usr/bin/env python3
"""
Quick Start Example for FFBB API Client V2

This example shows the simplest way to use the FFBB API Client V2
with automatic token management.

Prerequisites:
1. Install the package: pip install ffbb_api_client_v2
2. (Optional) Set up .env file for custom tokens
"""

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager


def main():
    """Quick start example with automatic token management."""

    print("FFBB API Client V2 - Quick Start")
    print("=" * 40)

    # Get tokens automatically (from env vars or FFBB API)
    print("\nFetching API tokens...")
    tokens = TokenManager.get_tokens()
    print("Tokens retrieved successfully!")

    # Create the API client
    client = FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )

    # Example 1: Search for basketball clubs in Paris
    print("\n1. Searching for clubs in Paris...")
    paris_clubs = client.search_organismes("Paris")
    hits = paris_clubs.hits or []
    print(f"   Found {len(hits)} clubs")

    # Example 2: Get detailed information about the first club
    if hits:
        club = hits[0]
        print(f"\n2. Getting details for: {club.nom}")

        if club.id is None:
            print("   Error: Club ID is None")
            return

        club_details = client.get_organisme(int(club.id))
        if club_details:
            print(f"   Name: {club_details.nom}")
            print(f"   Type: {club_details.type}")
            print(f"   Address: {club_details.adresse}")
            engagements = club_details.engagements
            teams_count = len(engagements) if engagements else 0
            print(f"   Teams: {teams_count}")

    # Example 3: Get current live matches
    print("\n3. Getting live matches...")
    lives = client.get_lives()
    print(f"   Currently {len(lives)} live matches")

    # Example 4: Get current seasons
    print("\n4. Getting current seasons...")
    seasons = client.get_saisons()
    active_seasons = [s for s in seasons if s.actif]
    print(f"   Found {len(active_seasons)} active seasons")

    print("\nQuick start completed!")
    print("Check out complete_usage_example.py for advanced features")


if __name__ == "__main__":
    main()
