from django.contrib import admin

from products import models


admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
admin.site.register(models.Review)
