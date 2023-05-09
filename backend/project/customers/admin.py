from django.contrib import admin

from customers import models


admin.site.register(models.Customer)
admin.site.register(models.CartItem)
admin.site.register(models.WishlistItem)
