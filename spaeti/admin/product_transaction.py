from django.contrib import admin

from spaeti.models import ProductTransaction


@admin.register(ProductTransaction)
class ProductTransactionAdmin(admin.ModelAdmin):
    pass
