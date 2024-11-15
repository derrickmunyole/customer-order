from django.http import QueryDict
from rest_framework.viewsets import ViewSet
from .serializers import OrderSerializer
from .models import Order
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status


class OrderViewSet(ViewSet):

    def list(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Order.objects.all()
        serializer = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializer(serializer)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            customer_id = request.data.get('customer')
            serializer.save(customer_id=customer_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        data = (
            request.data.dict()
            if isinstance(request.data, QueryDict) else request.data
        )
        serializer = OrderSerializer(order, data=data)
        if serializer.is_valid():
            print(f'From Update: {data}')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(f'Serializer errors: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
