from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product


User = get_user_model()


PENDING = "pending"
ACCEPTED = "accepted"
IN_PROCESS = "in_process"
SHIPPED = "shipped"
CANCELLED = "cancelled"
COMPLETED = "completed"

ORDER_STATUSES = (
    (PENDING, "Pending"),
    (ACCEPTED, "Accepted"),
    (IN_PROCESS, "In process"),
    (SHIPPED, "Shipped"),
    (CANCELLED, "Cancelled"),
    (COMPLETED, "Completed"),
)


class Order(models.Model):
    """
    Represents a single order made by user.
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True, default=None)
    date_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=ORDER_STATUSES, max_length=20, default=PENDING)

    class Meta:
        db_table = "orders"
        ordering = ["-date_ordered"]

    def __str__(self):
        return f"Order {self.id} ({self.user})"


class OrderDetail(models.Model):
    """
    Represents a single product type from the order.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="details")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    full_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = "order_details"

    def __str__(self):
        return f"{self.product} x{self.quantity}"


class Discount(models.Model):
    """
    Represents the discount connected to the order detail.
    """

    order_detail = models.OneToOneField(OrderDetail, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    discount_percent = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    date_gained = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        db_table = "discounts"
