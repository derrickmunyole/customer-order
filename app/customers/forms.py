from django import forms
from .models import Customer


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError('Phone number is required.')
        if len(phone) != 10:
            raise forms.ValidationError('Phone number must be 10 digits.')
        if not phone.isdigit():
            raise forms.ValidationError(
                'Phone number must contain only digits.'
            )
        return phone
