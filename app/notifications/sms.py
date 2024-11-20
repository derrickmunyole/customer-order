from django.conf import settings
import africastalking

# Initialize the SDK
africastalking.initialize(
    settings.AFRICASTALKING_USERNAME,
    settings.AFRICASTALKING_API_KEY
)

_client = africastalking.SMS


def send_sms(phone_number, message):
    """Send SMS using Africa's Talking gateway."""
    return _client.send(message, [phone_number])
