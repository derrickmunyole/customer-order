from django.test import TestCase
from django.urls import reverse, resolve
from authentication.views import login_view, auth_callback


class OIDCUrlsTest(TestCase):
    """
    Test suite for verifying OpenID Connect (OIDC) URL routing configurations.
    This class ensures that URLs related to OIDC authentication are correctly
    mapped to their corresponding view functions.
    """

    def test_login_url(self):
        """
        Test that the 'login' URL pattern is correctly mapped to login_view
        function.

        This test:
        1. Generates the URL using the 'login' URL name
        2. Verifies that the URL resolves to the login_view function
        """
        url = reverse('login')
        self.assertEqual(resolve(url).func, login_view)

    def test_callback_url(self):
        """
        Test that the OIDC callback URL pattern is correctly mapped to
        auth_callback function.

        This test:
        1. Generates the URL using the 'auth_callback' URL name
        2. Verifies that the URL resolves to the auth_callback function
        """
        url = reverse('auth_callback')
        self.assertEqual(resolve(url).func, auth_callback)
