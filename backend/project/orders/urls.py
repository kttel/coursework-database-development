from rest_framework import routers

from django.urls import path, include

from orders import views


router = routers.DefaultRouter()
router.register("orders", views.OrdersViewSet, "orders")

urlpatterns = [
    path("", include(router.urls)),
]
