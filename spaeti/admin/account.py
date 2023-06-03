from django.contrib import admin

from spaeti.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass
