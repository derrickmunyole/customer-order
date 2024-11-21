from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PhoneNumberForm


@login_required
def collect_phone_number(request):
    customer = request.user.customer

    if request.method == 'POST':
        form = PhoneNumberForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    else:
        form = PhoneNumberForm(instance=customer)

    return render(request, 'core/collect_phone.html', {'form': form})
