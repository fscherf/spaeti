from django.utils.html import format_html
from django.contrib import admin

from spaeti.models import AccountTransaction
from spaeti.utils import format_euro_amount


@admin.register(AccountTransaction)
class AccountTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'sender_account',
        'receiver_account',
        'product',
        'html_amount',
    )

    list_filter = (
        'date',
        'product',
        'sender_account',
        'receiver_account',
    )

    @admin.display(description='Amount')
    def html_amount(self, obj):
        return format_html(format_euro_amount(obj.amount, html=True))
