from django.shortcuts import render, redirect
from django.contrib.auth import logout
from allauth.account.views import LoginView
from django.urls import reverse
from .data import ITEM_LIST


# Frontend view for the homepage
def homepage(request):
    return render(request, 'core/home.html', {'items': ITEM_LIST})


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('customers:collect_phone_number')


def logout_view(request):
    logout(request)
    return redirect('/')
