from rest_framework import routers

from django.urls import path, include

from customers import views

router = routers.DefaultRouter()
router.register("wishlist", views.WishlistViewSet, basename="wishlist")
router.register("cart", views.CartViewSet, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
]
