from rest_framework import routers

from django.urls import path, include

from products import views

routers = routers.DefaultRouter()
routers.register("categories", views.CategoryViewSet, basename="categories")
routers.register("products", views.ProductViewSet, basename="products")
routers.register("reviews", views.DeleteReviewView, basename="reviews")


urlpatterns = [
    path("", include(routers.urls)),
    path("ingredients/", views.IngredientListAPIView.as_view()),
    path("tags/", views.TagListAPIView.as_view()),
]
