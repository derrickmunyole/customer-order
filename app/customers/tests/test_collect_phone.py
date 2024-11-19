from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from customers.models import Customer


class CollectPhoneNumberViewTests(TestCase):
    def setUp(self):
        # Create a test user and customer
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            name='Test Customer',
            code='TEST123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        self.url = reverse('customers:collect_phone_number')

    def test_get_phone_form(self):
        # Test that the form is displayed correctly
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/collect_phone.html')

    def test_valid_phone_number(self):
        # Test submission with valid Kenyan phone number
        response = self.client.post(self.url, {'phone': '0712345678'})
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.phone, '+254712345678')
        self.assertRedirects(response, reverse('core:home'))

    def test_unauthorized_access(self):
        # Test access without login
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
