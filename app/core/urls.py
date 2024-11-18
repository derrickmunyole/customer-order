from django.urls import path, include
from . import views

urlpatterns = [
    path('', view=views.homepage, name='home'),
    path('login', view=views.CustomLoginView.as_view(), name='login'),
    path("logout", view=views.logout_view, name='logout'),
    path('accounts/', include('allauth.urls')),
]
