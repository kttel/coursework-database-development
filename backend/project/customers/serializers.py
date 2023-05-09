from rest_framework import serializers

from customers import models
from products import serializers as pr_serializers


class WishlistItemsSerializer(serializers.ModelSerializer):
    product = pr_serializers.ProductSerializer(many=False, read_only=True)

    class Meta:
        model = models.WishlistItem
        exclude = ["customer"]


class CartItemsSerializer(serializers.ModelSerializer):
    product = pr_serializers.ProductSerializer(many=False, read_only=True)
    quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.CartItem
        exclude = ["customer"]
