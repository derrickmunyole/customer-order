from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'oidc_id', 'email']
