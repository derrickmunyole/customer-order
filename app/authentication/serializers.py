from rest_framework.serializers import ModelSerializer
from users.models import User


class OIDCUSerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['oidc_id', 'email']
