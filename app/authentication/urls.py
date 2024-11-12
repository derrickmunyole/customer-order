from django.urls import path
from . import views

urlpatterns = [
    path('login/', name='login', view=views.login_view),
    path('callback/', name='auth_callback', view=views.auth_callback)
]
