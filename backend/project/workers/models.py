from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Employee(models.Model):
    """
    Represents a single bakery worker.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "employees"

    def __str__(self):
        return self.title
