"""
URL mappings for orders app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, orders_view

app_name = 'orders'

router = DefaultRouter()
router.register('', viewset=OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('my-orders/', orders_view, name='orders-view'),
]
