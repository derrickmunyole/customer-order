from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from orders.models import Order
from users.models import User


class OrderAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            oidc_id='test_oidc_abbfa2c',
            email='test_user2@example.com'
        )

        self.customer = self.user.customer
        self.customer.name = 'Test Customer 2'
        self.customer.save()

        self.order = Order.objects.create(
            item="Item A",
            amount=99.99,
            quantity=2,
            customer=self.customer
        )
        self.list_url = reverse('order-list')
        self.detail_url = reverse('order-detail', args=[str(self.order.id)])

    def test_get_orders(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        data = {
            "item": "Item B",
            "amount": 50.00,
            "quantity": 1,
            "customer": self.customer.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_order(self):
        data = {
            "item": "Item B",
            "amount": 3,
            "quantity": 3
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
