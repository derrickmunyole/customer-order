from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class OIDCAuthTests(TestCase):
    """
    Test suite for OpenID Connect (OIDC) authentication functionality.
    Tests both the initial login redirect and callback handling.
    """

    def setup(self):
        """
        Initialize the test environment by setting up a test client.
        """
        self.client = Client()

    def test_login_view_redirects_to_provider(self):
        """
        Test that the login view properly redirects to the OIDC provider.

        Expected behavior:
        - When accessing the login URL
        - Should return a 302 (redirect) status code
        - Redirecting user to the OIDC provider's authorization endpoint
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)

    @patch('authentication.oauth.oauth.google.authorize_access_token')
    @patch('authentication.oauth.oauth.google.parse_id_token')
    def test_callback_view(self, mock_parse_token, mock_auth_token):
        """
        Test the OIDC callback view with mocked token responses.

        Args:
            mock_parse_token: Mock for the token parsing function
            mock_auth_token: Mock for the token authorization function

        Mocked data:
            - Access token: 'test_token'
            - ID token payload: Contains email and subject identifier

        Expected behavior:
            - Should process the callback successfully
            - Should return a 200 OK status code
        """
        mock_auth_token.return_value = {'token', 'test_token'}
        mock_parse_token.return_value = {
            'email': 'test@example.com',
            'sub': '12345'
        }

        response = self.client.get(reverse('auth_callback'))
        self.assertEqual(response.status_code, 200)
