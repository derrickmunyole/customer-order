from rest_framework.serializers import ModelSerializer
from .models import Order
from customers.serializers import CustomerSerializer
from customers.models import Customer


class OrderSerializer(ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'item', 'amount', 'quantity', 'customer', 'created_at']
        read_only = ['id', 'created_at']

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        customer = Customer.objects.get(pk=customer_id)
        order = Order.objects.create(customer=customer, **validated_data)
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
