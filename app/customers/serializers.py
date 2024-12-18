from rest_framework.serializers import ModelSerializer
from .models import Customer


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'code']
        read_only = ['id']
