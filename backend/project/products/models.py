from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    """
    Represents a category of products.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "categories"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Represents an ingredient used in end-products.
    """

    name = models.CharField(max_length=255)
    is_vegetarian = models.BooleanField(default=False)
    is_lactose_free = models.BooleanField(default=False)

    class Meta:
        db_table = "ingredients"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Represents a tag associated with products.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "tags"

    def __str__(self):
        return self.name


def get_image_path(instance, filename):
    return f"products/{instance.id}.jpg"


class Product(models.Model):
    """
    Represents a ready-to-sell dish.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price_per_one = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    image = models.ImageField(
        upload_to=get_image_path,
        default="products/default.png",
        blank=True,
        null=True,
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=False)
    available_amount = models.PositiveIntegerField(null=True, blank=True, default=0)
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.id is None:
            saved_image = self.image
            self.image = None
            super(Product, self).save(*args, **kwargs)
            self.profile_image = saved_image
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")

        super(Product, self).save(*args, **kwargs)

    class Meta:
        db_table = "products"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Represents a comment and a vote from user to the product.
    """

    VOTE_TYPE = (("up", "Up Vote"), ("down", "Down Vote"))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    body = models.TextField()
    value = models.CharField(max_length=10, choices=VOTE_TYPE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reviews"
        ordering = ["-date_added"]
        unique_together = [
            ["user", "product"],
        ]

    def __str__(self):
        return f"{self.value.upper()} to {self.product} by {self.user}"
