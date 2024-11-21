from rest_framework.serializers import ModelSerializer
from .models import Order
from customers.serializers import CustomerSerializer
from customers.models import Customer


class OrderListSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'item', 'amount', 'created_at']
        read_only = ['id', 'created_at']


class OrderSerializer(ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'item', 'amount', 'quantity', 'customer', 'created_at']
        read_only = ['id', 'created_at', 'customer']

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        return order

    def update(self, instance, validated_data):
        instance.item = validated_data.get('item', instance.item)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.quantity = validated_data.get('quantity', instance.quantity)

        if 'customer_id' in validated_data:
            customer_id = validated_data.pop('customer_id')
            instance.customer = Customer.objects.get(pk=customer_id)

        instance.save()
        return instance
