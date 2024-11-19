from django.test import TransactionTestCase
from django.db import transaction
from unittest.mock import patch
from django.contrib.auth import get_user_model
from orders.models import Order
from customers.models import Customer


class OrderNotificationSignalTests(TransactionTestCase):
    def setUp(self):

        User = get_user_model()

        self.user = User.objects.create_user(
            email="johnnytest@example.com",
            username="johnnytest"
        )
        self.customer = Customer.objects.create(
            user=self.user,
            name="Test Customer",
            phone="+254700000000"
        )

    @patch('notifications.sms.send_sms')
    def test_sms_sent_on_order_creation(self, mock_send_sms):
        """Test that SMS is sent when a new order is created"""
        order = Order.objects.create(
            customer=self.customer,
            item="Test Item",
            amount=100,
            quantity=1
        )

        # Execute any pending on_commit callbacks
        for func in transaction.get_connection().run_on_commit:
            func()

        # The mock assertion needs to happen after the transaction.on_commit
        #  callback executes
        mock_send_sms.assert_called_once_with(
            self.customer.phone,
            f"Your order #{order.id} has been placed successfully"
        )

    @patch('notifications.sms.send_sms')
    def test_sms_not_sent_on_order_update(self, mock_send_sms):
        """Test that SMS is not sent when an order is updated"""
        # Create order first
        order = Order.objects.create(
            customer=self.customer,
            item="Test Item",
            amount=100,
            quantity=1
        )

        # Reset the mock to clear the creation call
        mock_send_sms.reset_mock()

        # Update the order
        order.amount = 200
        order.save()

        # Force the transaction to commit
        transaction.commit()

        # Verify no SMS was sent
        mock_send_sms.assert_not_called()

    @patch('notifications.sms.send_sms')
    def test_sms_handles_error_gracefully(self, mock_send_sms):
        """Test that SMS errors don't affect order creation"""
        # Make the SMS service raise an exception
        mock_send_sms.side_effect = Exception("SMS Service Error")

        # Create order should still succeed
        order = Order.objects.create(
            customer=self.customer,
            item="Test Item",
            amount=100,
            quantity=1
        )

        # Force the transaction to commit
        transaction.commit()

        # Verify order was created despite SMS failure
        self.assertTrue(Order.objects.filter(id=order.id).exists())
        mock_send_sms.assert_called_once()
