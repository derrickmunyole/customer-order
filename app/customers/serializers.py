from rest_framework.serializers import ModelSerializer
from .models import Customer
from users.serializers import UserSerializer


class CustomerSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'user', 'name', 'phone', 'code']
        read_only = ['id']
