from django.test import TestCase
from users.models import User
from customers.models import Customer


class CustomerSignalTest(TestCase):
    # creating new user
    def customer_entry_on_user_save(self):
        user = User.objects.create(
            email="johnnytest@example.com",
            oidc_id="test123"
        )

        # check if customer is automatically created

        try:
            customer = Customer.objects.get(user=user)
            self.assertIsInstance(customer, Customer)
            self.assertEqual(customer.user, user)
            self.assertEqual(customer.name, '')
            self.assertEqual(customer.code, '')
            self.assertEqual(customer.Phone, '')
        except Customer.DoesNotExist:
            self.fail("Customer wasn't created during user save")

    def test_customer_is_unique_per_user_entry(self):
        # create a new user verifying only one customer entry corresponding to
        # created user
        user = User.objects.create(
            email="johnnytest@example.com",
            oidc_id="test123"
        )

        customer_count = Customer.objects.filter(user=user).count()
        self.assertEqual(customer_count, 1)
