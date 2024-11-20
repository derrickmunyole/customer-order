from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import Customer
from uuid import uuid4


@receiver(user_signed_up)
def create_customer_profile(sender, request, user, **kwargs):
    """
    Signal receiver that creates a Customer profile when a new user signs up.

    This function is triggered after a successful user registration. It checks
    if a Customer profile already exists for the user, and if not, creates one.
    The customer name is extracted from social account data if available,
    otherwise defaults to username. A unique customer code is generated for
    each new customer.

    Args:
        sender: The sender of the signal (usually the User model)
        request: The HTTP request object
        user: The User instance that was just created
        **kwargs: Additional keyword arguments passed with the signal

    Returns:
        None

    Side Effects:
        - Creates a new Customer object in the database if one doesn't exist
          for the user
    """
    if not Customer.objects.filter(user=user).exists():
        social_account = user.socialaccount_set.first()
        if social_account:
            extra_data = social_account.extra_data
            name = extra_data.get('name', user.username)
        else:
            name = user.username

        customer_code = str(uuid4())[:8].upper()

        Customer.objects.create(
            user=user,
            name=name,
            code=customer_code
        )
