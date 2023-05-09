from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.generics import ListAPIView
from rest_framework import views, status, permissions, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from products import models, serializers
from customers import models as cu_models


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    lookup_field = "slug"
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def retrieve(self, request, slug=None):
        products = models.Product.objects.filter(category__slug=slug)
        serializer = serializers.ProductDetailSerializer(products, many=True)
        return Response(serializer.data)


class TagListAPIView(ListAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class IngredientListAPIView(ListAPIView):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        result = super().list(request, *args, **kwargs)
        data = result.data
        page = int(self.request.query_params.get("page", 1))
        previous_page = (page - 1) if data["previous"] is not None else None
        next_page = (page + 1) if data["next"] is not None else None
        page_size = self.pagination_class.page_size
        data.update(
            {
                "page": page,
                "previous_page": previous_page,
                "next_page": next_page,
                "page_size": page_size,
            }
        )
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=("post",), detail=True)
    def order(self, request, pk=None):
        quantity = request.data.get("quantity")

        try:
            quantity = int(quantity)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if quantity <= 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        product = models.Product.objects.get(pk=pk)
        if product.available_amount < quantity:
            return Response(
                {"message": "There aren't enough products"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cu_models.CartItem.objects.create(
            customer=request.user.customer,
            product=product,
            quantity=quantity,
        )

        product.available_amount = product.available_amount - quantity
        if product.available_amount == 0:
            product.is_available = False
        product.save()

        return Response(
            data={"message": "Product was succesfully added to the cart!"},
            status=status.HTTP_201_CREATED,
        )

    @action(methods=("post",), detail=True)
    def wish(self, request, pk=None):
        payload = {
            "customer": request.user.customer,
            "product": models.Product.objects.get(pk=pk),
        }
        obj, _ = cu_models.WishlistItem.objects.get_or_create(**payload)
        return Response(
            data={"product": obj.product.name},
            status=status.HTTP_200_OK,
        )

    @action(methods=("post",), detail=True)
    def review(self, request, pk=None):
        try:
            body = request.data.get("body")
            value = request.data.get("value")
            if not body or value not in ["up", "down"]:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            product = models.Product.objects.get(pk=pk)
            models.Review.objects.create(
                user=request.user,
                product=product,
                body=body,
                value=value,
            )
            product.vote_total += 1
            good_votes = models.Review.objects.filter(
                product=product,
                value="up",
            ).count()
            total_votes = models.Review.objects.filter(
                product=product,
            ).count()
            product.vote_ratio = good_votes / total_votes * 100
            product.save()
            return Response(
                data={"message": "Review was successfully created"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "order":
            return serializers.OrderProductSerializer
        if self.action == "wish":
            return serializers.WishProductSerializer
        if self.action == "review":
            return serializers.ReviewSerializer
        if self.action == "retrieve":
            return serializers.ProductDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        category = self.request.query_params.get("category")
        if category:
            return models.Product.objects.filter(category__slug=category)
        return self.queryset


class DeleteReviewView(mixins.DestroyModelMixin, GenericViewSet):
    model = models.Review
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.BlankSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Review.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        product = review.product
        product.vote_total -= 1
        good_votes = models.Review.objects.filter(
            product=product,
            value="up",
        ).count()
        total_votes = models.Review.objects.filter(
            product=product,
        ).count()
        product.vote_ratio = good_votes / total_votes * 100
        product.save()
        result = super().destroy(request, *args, **kwargs)
        return result
