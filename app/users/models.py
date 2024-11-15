from django.db import models
from uuid import uuid4


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    oidc_id = models.CharField(max_length=60)
    email = models.EmailField(max_length=50, unique=True)
