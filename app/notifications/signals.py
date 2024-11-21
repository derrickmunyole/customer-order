from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from django.db import transaction
from . import sms


@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    """
    Signal handler that sends SMS notification when a new order is created.

    Uses Django's transaction.on_commit to ensure the SMS is sent only after
    the database transaction is successfully committed. This prevents
    notifications from being sent if the transaction fails.

    Args:
        sender: The model class (Order)
        instance: The actual Order instance that was saved
        created: Boolean indicating if this is a new order
        **kwargs: Additional arguments passed by the signal

    Note:
        SMS errors are caught and logged but don't affect the order creation.
    """
    if created:
        def send_notification():
            try:
                sms.send_sms(
                    instance.customer.phone,
                    f"Your order #{instance.id} has been placed successfully"
                )
                print("SMS Sent")
            except Exception as e:
                print(f"SMS notification failed: {str(e)}")

        transaction.on_commit(send_notification)
