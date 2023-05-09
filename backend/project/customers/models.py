from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from products.models import Product


User = get_user_model()


class Customer(models.Model):
    """
    Represents the client connected to the registered user.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = "customers"

    def __str__(self) -> str:
        return self.user.email


class CartItem(models.Model):
    """
    Represents the item from user's cart.
    """

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cart_items"

    def __str__(self):
        return f"{self.product.name} for {self.customer.user}"


class WishlistItem(models.Model):
    """
    Represents the item from user's wishlist.
    """

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wishlist_items"

    def __str__(self):
        return f"{self.product.name} for {self.customer.user}"
