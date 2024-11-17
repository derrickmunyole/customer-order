from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import Customer
from uuid import uuid4


@receiver(user_signed_up)
def create_customer_profile(sender, request, user, **kwargs):
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
