from .base import FunctionalTest
from customers.models import Customer
from django.contrib.auth.models import User
from unittest.mock import patch


class OrderManagementTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        # Create test user first
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Create test customer associated with user
        self.customer = Customer.objects.create(
            user=self.user,
            name='Test Customer',
            phone='+254700000000'  # Add test phone number
        )
        # Login the user
        self.client.login(username='testuser', password='testpass123')

    @patch('notifications.signals.sms.send_sms')
    def test_can_create_order_and_send_sms(self, mock_send_sms):
        # Get the session cookie and add it to selenium
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({
            'name': 'sessionid',
            'value': cookie.value,
            'secure': False,
            'path': '/'
        })

        # Test order creation
        response = self.client.post('/api/orders/', {
            'item': 'Test Item',
            'amount': 100.00,
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)

        # Verify SMS was triggered
        mock_send_sms.assert_called_once()
        # Verify SMS was called with correct parameters
        call_args = mock_send_sms.call_args[0]  # Get positional arguments
        self.assertEqual(call_args[0], self.customer.phone)  # Check phone number
        self.assertIn('has been placed successfully', call_args[1])  # Check message
