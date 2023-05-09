from rest_framework import views, viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db import connection

from orders import models, serializers


class OrdersViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    model = models.Order
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    @action(methods=("post",), detail=False)
    def cancel(self, request):
        user = request.user
        orders = models.Order.objects.filter(status="pending")
        if orders.exists():
            with connection.cursor() as cursor:
                cursor.execute(f"EXEC cancelOrders @customer_id = {user.pk}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"response": "No orders to cancel"}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=("post",), detail=True)
    def cancel_single(self, request, pk=None):
        order = models.Order.objects.get(pk=pk)
        if order.status == "pending":
            order.status = "cancelled"
            order.save()
            serializer = serializers.OrderSerializer(order)
            return Response({**serializer.data, "id": pk}, status=status.HTTP_200_OK)
        return Response(
            {"response": "Order can't be cancelled"}, status=status.HTTP_400_BAD_REQUEST
        )

    def get_queryset(self):
        user = self.request.user
        return models.Order.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.OrderWithDetailsSerializer
        if self.action == "cancel" or self.action == "cancel_single":
            return serializers.OrderCancelSerializer
        return self.serializer_class
