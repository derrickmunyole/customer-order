from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiResponse
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError as DjangoValidationError
from psycopg2.errors import IntegrityError
from rest_framework.response import Response
from rest_framework import status, serializers
from django.shortcuts import get_object_or_404

from orders import serializers as orders_serializers
from customers.models import Customer
from .models import Order

import logging
logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        summary="List all orders",
        description="Returns a list of orders for the authenticated user",
        responses={
            200: orders_serializers.OrderListSerializer(many=True),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Orders"]
    ),
    retrieve=extend_schema(
        summary="Get order details",
        description="Returns details of a specific order",
        responses={
            200: orders_serializers.OrderSerializer,
            404: OpenApiResponse(description="Order not found"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Orders"]
    ),
    create=extend_schema(
        summary="Create new order",
        description="Create a new order for the authenticated user",
        request=orders_serializers.OrderSerializer,
        responses={
            201: orders_serializers.OrderSerializer,
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Orders"]
    ),
    update=extend_schema(
        summary="Update order",
        description="Update an existing order",
        request=orders_serializers.OrderSerializer,
        responses={
            200: orders_serializers.OrderSerializer,
            400: OpenApiResponse(description="Bad request"),
            404: OpenApiResponse(description="Order not found"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Orders"]
    ),
    destroy=extend_schema(
        summary="Delete order",
        description="Delete an existing order",
        responses={
            204: OpenApiResponse(description="Order deleted successfully"),
            404: OpenApiResponse(description="Order not found"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Orders"]
    ),
)
class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = orders_serializers.OrderSerializer

    queryset = Order.objects.all()

    def get_serializer_class(self):
        """
        Get the serializer class for the request
        """
        if self.action == 'list':
            return orders_serializers.OrderListSerializer

        return self.serializer_class

    def get_queryset(self):
        """Fetch orders for authenticated users"""
        return self.queryset.filter(customer=self.request.user.customer).order_by('-id')

    def list(self, request):
        """Return list of orders for authenticated user"""
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Return a specific order"""
        order = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    from psycopg2.errors import IntegrityError

    def perform_create(self, serializer):
        """Create a new order with exception handling."""
        try:
            user = self.request.user
            customer, created = Customer.objects.get_or_create(
                user=user,
                defaults={
                    'name': user.username
                }
            )
            serializer.save(customer=customer)
        except (IntegrityError, DjangoValidationError, KeyError, Exception) as e:
            # Log the detailed error for debugging
            logger.error(f"Error creating order: {str(e)}")
            # Return a generic error message to the client
            raise serializers.ValidationError({
                "error": "Unable to process your order. Please try again later."
            })

    def update(self, request, pk=None):
        """Update an order with exception handling"""
        order = get_object_or_404(self.get_queryset(), pk=pk)
        try:
            serializer = self.get_serializer(order, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except DjangoValidationError as e:
            logger.error(f"Validation error while updating order: {str(e)}")
            raise serializers.ValidationError({
                "error": "Invalid data for order update"
            })

    def destroy(self, request, pk=None):
        """Delete an order"""
        order = get_object_or_404(self.get_queryset(), pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
