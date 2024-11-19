from django.test import TestCase
from django.contrib.auth import get_user_model
from customers.models import Customer
from allauth.socialaccount.models import SocialAccount


class CustomerSignalTest(TestCase):
    def test_customer_creation_with_social_account(self):
        # Create a user using get_user_model
        User = get_user_model()
        user = User.objects.create(
            email="johnnytest@example.com",
            username="johnnytest"
        )

        # Create a mock social account
        SocialAccount.objects.create(
            user=user,
            provider='google',
            extra_data={
                'name': 'Johnny Test'
            }
        )

        # Simulate the user_signed_up signal
        from allauth.account.signals import user_signed_up
        user_signed_up.send(
            sender=User,
            request=None,
            user=user
        )

        # Check if customer is automatically created
        try:
            customer = Customer.objects.get(user=user)
            self.assertIsInstance(customer, Customer)
            self.assertEqual(customer.user, user)
            self.assertEqual(customer.name, 'Johnny Test')
        except Customer.DoesNotExist:
            self.fail("Customer wasn't created during user sign up")

    def test_customer_creation_without_social_account(self):
        # Create a user using get_user_model
        User = get_user_model()
        user = User.objects.create(
            email="johnnytest@example.com",
            username="johnnytest"
        )

        # Simulate the user_signed_up signal
        from allauth.account.signals import user_signed_up
        user_signed_up.send(
            sender=User,
            request=None,
            user=user
        )

        # Check if customer is created with fallback username
        try:
            customer = Customer.objects.get(user=user)
            self.assertIsInstance(customer, Customer)
            self.assertEqual(customer.user, user)
            self.assertEqual(customer.name, 'johnnytest')
        except Customer.DoesNotExist:
            self.fail("Customer wasn't created during user sign up")

    def test_customer_is_unique_per_user_signup(self):
        # Create a user using get_user_model
        User = get_user_model()
        user = User.objects.create(
            email="johnnytest@example.com",
            username="johnnytest"
        )

        # Simulate the user_signed_up signal
        from allauth.account.signals import user_signed_up
        user_signed_up.send(
            sender=User,
            request=None,
            user=user
        )

        # Trigger the signal again to test uniqueness
        user_signed_up.send(
            sender=User,
            request=None,
            user=user
        )

        customer_count = Customer.objects.filter(user=user).count()
        self.assertEqual(customer_count, 1)
