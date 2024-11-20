from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal
from customers.models import Customer
from orders.models import Order


class OrderModelTests(TestCase):
    def setUp(self):
        # Create a test user first
        User = get_user_model()
        user = User.objects.create(
            email="johnnytest@example.com",
            username="johnnytest"
        )

        # Now create the customer with the user
        self.customer = Customer.objects.create(
            name="Test Customer",
            user=user  # Associate the user with the customer
        )

    def test_create_order_success(self):
        """Test creating an order with valid data"""
        order = Order.objects.create(
            item="Test Item",
            amount=Decimal('99.99'),
            quantity=2,
            customer=self.customer
        )
        self.assertEqual(order.item, "Test Item")
        self.assertEqual(order.amount, Decimal('99.99'))
        self.assertEqual(order.quantity, 2)

    def test_string_representation(self):
        """Test the string representation of the Order model"""
        order = Order.objects.create(
            item="Test Item",
            amount=Decimal('99.99'),
            quantity=2,
            customer=self.customer
        )
        expected_string = f'Order #{order.id}: ({self.customer.name})'
        self.assertEqual(str(order), expected_string)

    def test_quantity_validators(self):
        """Test quantity validators (min=1, max=10)"""
        # Test quantity below minimum
        with self.assertRaises(ValidationError):
            order = Order.objects.create(
                item="Test Item",
                amount=Decimal('99.99'),
                quantity=0,
                customer=self.customer
            )
            order.full_clean()

        # Test quantity above maximum
        with self.assertRaises(ValidationError):
            order = Order.objects.create(
                item="Test Item",
                amount=Decimal('99.99'),
                quantity=11,
                customer=self.customer
            )
            order.full_clean()

    def test_cascade_delete(self):
        """Test that orders are deleted when customer is deleted"""
        order = Order.objects.create(
            item="Test Item",
            amount=Decimal('99.99'),
            quantity=2,
            customer=self.customer
        )

        # Delete customer and verify order is also deleted
        self.customer.delete()
        self.assertEqual(Order.objects.filter(id=order.id).count(), 0)

    def test_item_max_length(self):
        """Test that item field enforces max_length of 100"""
        order = Order(
            item="x" * 101,  # Create string longer than max_length
            amount=Decimal('99.99'),
            quantity=2,
            customer=self.customer
        )

        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_amount_decimal_places(self):
        """Test amount field decimal place constraint"""
        with self.assertRaises(ValidationError):
            order = Order.objects.create(
                item="Test Item",
                amount=Decimal('99.999'),  # More than 2 decimal places
                quantity=2,
                customer=self.customer
            )
            order.full_clean()

    def test_created_at_auto_set(self):
        """Test that created_at is automatically set"""
        order = Order.objects.create(
            item="Test Item",
            amount=Decimal('99.99'),
            quantity=2,
            customer=self.customer
        )
        self.assertIsNotNone(order.created_at)
