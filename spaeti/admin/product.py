from django.contrib import admin

from spaeti.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
