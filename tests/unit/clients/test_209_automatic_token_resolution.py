import unittest
from unittest.mock import patch

from ffbb_api_client_v3.clients.ffbb_api_client_v3 import FFBBAPIClientV3
from ffbb_api_client_v3.utils.token_manager import FFBBTokens


class TestAutomaticTokenResolution(unittest.TestCase):
    @patch("ffbb_api_client_v3.utils.token_manager.TokenManager.get_tokens")
    def test_create_without_tokens(self, mock_get_tokens):
        # Mock tokens
        mock_get_tokens.return_value = FFBBTokens(
            api_token="auto_api_token_123", meilisearch_token="auto_ms_token_123"
        )

        # Create client without providing tokens
        client = FFBBAPIClientV3.create()

        # Verify TokenManager was called
        mock_get_tokens.assert_called_once()

        # Verify client has the expected tokens
        self.assertEqual(client.api_ffbb_client.bearer_token, "auto_api_token_123")
        self.assertEqual(
            client.meilisearch_ffbb_client.bearer_token, "auto_ms_token_123"
        )

    @patch("ffbb_api_client_v3.utils.token_manager.TokenManager.get_tokens")
    def test_create_with_one_token_missing(self, mock_get_tokens):
        # Mock tokens
        mock_get_tokens.return_value = FFBBTokens(
            api_token="auto_api_token_123", meilisearch_token="auto_ms_token_123"
        )

        # Create client with only one token
        client = FFBBAPIClientV3.create(api_bearer_token="manual_api_token")

        # Verify TokenManager was called
        mock_get_tokens.assert_called_once()

        # Verify client has mixed tokens
        self.assertEqual(client.api_ffbb_client.bearer_token, "manual_api_token")
        self.assertEqual(
            client.meilisearch_ffbb_client.bearer_token, "auto_ms_token_123"
        )


if __name__ == "__main__":
    unittest.main()
