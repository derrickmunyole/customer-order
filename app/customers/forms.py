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

        # Basic validation before conversion
        if not phone.replace('+', '').isdigit():
            raise forms.ValidationError(
                'Phone number must contain only digits.'
            )

        # Remove any spaces or special characters
        phone = ''.join(filter(str.isdigit, phone))

        # Validate original input length (should be 10 digits for local format)
        if phone.startswith('0') and len(phone) != 10:
            raise forms.ValidationError('Phone number must be 10 digits.')

        # Handle different input formats
        if phone.startswith('0'):
            phone = '+254' + phone[1:]
        elif phone.startswith('254'):
            phone = '+' + phone
        elif not phone.startswith('+254'):
            raise forms.ValidationError(
                'Please enter a valid Kenyan phone number'
            )

        # Validate the final length (should be 13 characters for +254XXXXXXXXX)
        if len(phone) != 13:
            raise forms.ValidationError(
                'Phone number must be 9 digits after the country code'
            )

        return phone
