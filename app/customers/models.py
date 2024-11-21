from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=True)
    phone = models.CharField(max_length=13, null=True)
    code = models.CharField(max_length=20, null=True)

    def __str__(self) -> str:
        return f'{self.name} ({self.code})'
