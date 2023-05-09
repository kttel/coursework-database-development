from rest_framework import serializers

from orders import models
from products import serializers as pr_serializers


class OrderDetailSerializer(serializers.ModelSerializer):
    product = pr_serializers.ProductDetailSerializer(many=False, read_only=True)

    class Meta:
        model = models.OrderDetail
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        exclude = ["user"]


class OrderWithDetailsSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)

    class Meta:
        model = models.Order
        exclude = ["user"]
        related_object = "order_detail"


class OrderCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ["id"]
