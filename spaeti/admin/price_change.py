from django.contrib import admin

from spaeti.models import PriceChange


@admin.register(PriceChange)
class PriceChangeAdmin(admin.ModelAdmin):
    pass
