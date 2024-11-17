from django.urls import path
from . import views

urlpatterns = [
    path(
        'collect-phone/',
        views.collect_phone_number,
        name='collect_phone_number'),
]
