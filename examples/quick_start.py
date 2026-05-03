#!/usr/bin/env python3
"""
Quick Start Example for FFBB API Client V2

This example shows the simplest way to use the FFBB API Client V2
with automatic token management.

Prerequisites:
1. Install the package: pip install ffbb_data_client
2. (Optional) Set up .env file for custom tokens

Features demonstrated:
- Automatic token resolution
- Basic API operations (search, get details, live matches, seasons)
- Error handling patterns
- Clean resource management
"""

import sys

from ffbb_data_client import FFBBDataClient, TokenManager


def main():
    """Quick start example with automatic token management and error handling."""

    print("FFBB API Client V2 - Quick Start")
    print("=" * 40)

    try:
        # Step 1: Get tokens automatically (from env vars or FFBB API)
        print("\n🔑 Fetching API tokens...")
        tokens = TokenManager.get_tokens()
        print("✅ Tokens retrieved successfully!")

        # Step 2: Create the API client
        print("\n🔧 Creating API client...")
        client = FFBBDataClient.create(
            api_bearer_token=tokens.api_token,
            meilisearch_bearer_token=tokens.meilisearch_token,
        )
        print("✅ Client initialized successfully!")

        # Example 1: Search for basketball clubs in Paris
        print("\n1️⃣ Searching for clubs in Paris...")
        try:
            paris_clubs = client.search_organismes("Paris")
            if paris_clubs is None:
                print("   ❌ Search returned None")
                return

            hits = paris_clubs.hits or []
            print(f"   ✅ Found {len(hits)} clubs")

            # Example 2: Get detailed information about the first club
            if hits:
                club = hits[0]
                print(f"\n2️⃣ Getting details for: {club.nom}")

                if club.id is None:
                    print("   ⚠️ Club ID is None, skipping details")
                    return

                club_details = client.get_organisme(int(club.id))
                if club_details:
                    print(f"   ✅ Basic info: {club_details.nom}")
                    print(f"   📍 Type: {club_details.type}")
                    print(f"   🏠 Address: {club_details.adresse}")

                    # Show team count safely
                    engagements = club_details.engagements
                    teams_count = len(engagements) if engagements else 0
                    print(f"   👥 Teams: {teams_count}")
                else:
                    print("   ❌ Failed to get club details")
            else:
                print("   ℹ️ No clubs found in Paris")

        except Exception as e:
            print(f"   ❌ Search failed: {e}")
            return

        # Example 3: Get current live matches
        print("\n3️⃣ Getting live matches...")
        try:
            lives = client.get_lives()
            if lives is None:
                print("   ❌ Live matches returned None")
                return
            print(f"   ⚽ Currently {len(lives)} live matches")

            # Show a few examples if available
            if lives:
                for i, live in enumerate(lives[:3]):  # Show max 3
                    print(
                        f"      {i + 1}. {live.team_name_home} vs {live.team_name_out}"
                    )

        except Exception as e:
            print(f"   ❌ Live matches failed: {e}")

        # Example 4: Get current seasons
        print("\n4️⃣ Getting current seasons...")
        try:
            seasons = client.get_saisons()
            if seasons is None:
                print("   ❌ Seasons returned None")
                return
            active_seasons = [s for s in seasons if getattr(s, "actif", False)]
            print(f"   📅 Found {len(active_seasons)} active seasons")

            # Show season names
            for season in active_seasons[:3]:  # Show max 3
                print(f"      • {getattr(season, 'nom', 'Unknown')}")

        except Exception as e:
            print(f"   ❌ Seasons failed: {e}")

        print("\n🎉 Quick start completed successfully!")
        print("\n💡 Next steps:")
        print("   • Run complete_usage_example.py for advanced features")
        print("   • Check examples/README.md for more examples")
        print("   • Read the full documentation in docs/")

    except ValueError as e:
        print(f"\n❌ Configuration error: {e}")
        print("💡 Make sure your environment is set up correctly")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Check your internet connection and API status")
        sys.exit(1)


if __name__ == "__main__":
    main()
