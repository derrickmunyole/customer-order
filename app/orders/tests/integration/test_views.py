from django.urls import reverse
from django.test import Client
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from orders.models import Order
from customers.models import Customer
from unittest.mock import patch
from psycopg2.errors import IntegrityError
from uuid import uuid4


User = get_user_model()


class OrderAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            name='Test Customer'
        )

        self.client.force_login(user=self.user)

        # Create test order
        self.order = Order.objects.create(
            item="Item A",
            amount=99.99,
            quantity=2,
            customer=self.customer
        )

        self.list_url = reverse('orders:order-list')
        self.detail_url = reverse(
            'orders:order-detail', args=[str(self.order.id)]
            )

    def test_get_orders(self):
        """Test retrieving authenticated user's orders"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['item'], "Item A")

    def test_create_order(self):
        """Test creating an order for authenticated user"""
        data = {
            "item": "Item B",
            "amount": 50.00,
            "quantity": 1,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['item'], "Item B")
        self.assertEqual(
            response.data['customer'].get('id'), str(self.customer.id)
            )

    def test_create_order_invalid_data(self):
        """Test order creation with invalid data"""
        data = {
            "item": "",  # Invalid empty item
            "amount": -50.00,  # Invalid negative amount
            "quantity": 0,  # Invalid zero quantity
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order(self):
        """Test updating an order"""
        data = {
            "item": "Updated Item",
            "amount": 75.00,
            "quantity": 3
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['item'], "Updated Item")
        self.assertEqual(response.data['quantity'], 3)

    def test_delete_order(self):
        """Test deleting an order"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_unauthorized_access(self):
        """Test unauthenticated user cannot access orders"""
        # Create a new client instance without authentication
        client = Client()

        # Attempt to access orders endpoint
        response = client.get('/orders/')

        # Endpoint returns 401 Unauthorized for unauthenticated requests
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_integrity_error(self):
        """Test order creation with integrity error"""
        # Mock IntegrityError scenario
        with patch(
            'orders.views.Customer.objects.get_or_create'
                ) as mock_get_or_create:
            mock_get_or_create.side_effect = IntegrityError()
            data = {
                "item": "Test Item",
                "amount": 50.00,
                "quantity": 1,
            }
            response = self.client.post(self.list_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                response.data['error'],
                "Unable to process your order. Please try again later."
            )

    def test_get_nonexistent_order(self):
        """Test retrieving a non-existent order returns 404"""
        non_existent_uuid = str(uuid4())
        non_existent_url = reverse(
            'orders:order-detail', args=[non_existent_uuid]
            )
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_order_invalid_data(self):
        """Test updating order with invalid data"""
        data = {
            "item": "",
            "amount": -100.00,
            "quantity": 0
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_access_other_user_order(self):
        """Test user cannot access another user's order"""
        # Create another user and order
        other_user = User.objects.create(
            username='other', email='other@example.com'
            )
        other_customer = Customer.objects.create(
            user=other_user, name='Other Customer'
            )
        other_order = Order.objects.create(
            item="Other Item",
            amount=99.99,
            quantity=1,
            customer=other_customer
        )
        other_detail_url = reverse(
            'orders:order-detail', args=[str(other_order.id)]
            )

        response = self.client.get(other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
