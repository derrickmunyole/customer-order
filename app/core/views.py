from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .data import ITEM_LIST


# Frontend view for the homepage
def homepage(request):
    return render(request, 'core/home.html', {'items': ITEM_LIST})


def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/')
