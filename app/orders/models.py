from django.db import models
from uuid import uuid4
from customers.models import Customer
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):
    """
    Represents an order in the system.

    This model stores information about customer orders including the item
    ordered, its amount, quantity, and associated customer details.

    Attributes:
        id (UUIDField): Unique identifier for the order using UUID4.
        item (CharField): Name or description of the ordered item, limited to
        100 characters.
        amount (DecimalField): Price of the item, supports up to 4 digits with
        2 decimal places.
        quantity (IntegerField): Number of items ordered, must be between 1
        and 10.
        customer (ForeignKey): Reference to the Customer model who placed the
        order.
        created_at (DateTimeField): Timestamp when the order was created.

    Relationships:
        - One-to-Many relationship with Customer model (many orders can belong
          to one customer)
        - Cascading delete: if a customer is deleted, their orders will also
          be deleted

    Example:
        order = Order.objects.create(
            item="Product Name",
            amount=99.99,
            quantity=2,
            customer=customer_instance
        )
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    item = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=4, decimal_places=2)
    quantity = models.IntegerField(
        null=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders'
        )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Returns a string representation of the Order.

        Returns:
            str: A string in the format 'Order #<uuid>: (<customer_name>)'
        """
        return f'Order #{self.id}: ({self.customer.name})'
