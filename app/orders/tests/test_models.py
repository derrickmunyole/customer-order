from users.models import User
from django.test import TestCase
from orders.models import Order


class OrderModelTests(TestCase):
    def setUp(self):

        self.user = User.objects.create(
            oidc_id='test_oidc_abbeaoc',
            email='test_user@example.com'
        )

        self.customer = self.user.customer
        self.customer.name = 'Test Customer'
        self.customer.save()

        self.order = Order.objects.create(
            item="Item A",
            amount=99.99,
            quantity=2,
            customer=self.customer
        )

    def test_order_creation(self):
        self.assertTrue(isinstance(self.order, Order))

        # Check if the customer name was explicitly set in the test setup
        if self.customer.name:
            expected_str = f'Order #{self.order.id}: ({self.customer.name})'
        else:
            expected_str = (
                f'Order #{self.order.id}: (Customer for {self.user.email})'
            )

        self.assertEqual(str(self.order), expected_str)
