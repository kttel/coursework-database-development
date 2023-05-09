from rest_framework import serializers, exceptions

from products import models
from users import serializers as u_serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        lookup_field = "slug"
        fields = "__all__"


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = "__all__"


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        exclude = (
            "ingredients",
            "date_modified",
            "available_amount",
            "date_added",
        )


class ReviewSerializer(serializers.ModelSerializer):
    user = u_serializers.UserSerializer(many=False, read_only=True)

    class Meta:
        model = models.Review
        fields = "__all__"


class ProductDetailSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = "__all__"


class OrderProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()


class WishProductSerializer(serializers.Serializer):
    pass


class BlankSerializer(serializers.Serializer):
    pass
