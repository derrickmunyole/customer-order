from rest_framework.serializers import ModelSerializer
from .models import Order
from customers.serializers import CustomerSerializer


class OrderSerializer(ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'item', 'amount', 'quantity', 'customer', 'created_at']
        read_only = ['id', 'created_at']
