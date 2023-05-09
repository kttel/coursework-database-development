from rest_framework import viewsets, permissions, views, mixins, status
from rest_framework.response import Response

from customers import models, serializers
from orders import models as or_models


class WishlistViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    model = models.WishlistItem
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.WishlistItemsSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return models.WishlistItem.objects.filter(customer=user.customer)


class CartViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    model = models.CartItem
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CartItemsSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return models.CartItem.objects.filter(customer=user.customer)

    def create(self, request, *args, **kwargs):
        user = request.user
        order = or_models.Order.objects.create(user=user)
        cart_queryset = self.get_queryset()
        for item in cart_queryset:
            or_models.OrderDetail.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                full_price=(item.product.price_per_one * item.quantity),
            )
            item.delete()
        return Response(status=status.HTTP_201_CREATED)
