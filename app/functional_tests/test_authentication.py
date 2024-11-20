from .base import FunctionalTest
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs
from unittest.mock import patch


class AuthenticationTest(FunctionalTest):
    @patch('allauth.socialaccount.providers.google.views.oauth2_login')
    def test_login_with_openid_connect(self, mock_oauth_login):
        # Navigate to login page
        self.browser.get(f'{self.live_server_url}/login')

        # Find and click the sign-in button
        sign_in_button = self.browser.find_element(By.ID, 'sign-in')
        sign_in_button.click()

        # Verify OAuth parameters without making real calls
        current_url = self.browser.current_url
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)

        self.assertIn('client_id', query_params)
        self.assertIn('redirect_uri', query_params)
