from django.utils.html import format_html
from django.contrib import admin

from spaeti.models import BankAccountTransaction
from spaeti.utils import format_euro_amount


@admin.register(BankAccountTransaction)
class BankAccountTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'bank_account',
        'receiver_bank_account',
        'product',
        'html_amount',
        'html_balance',
    )

    list_filter = (
        'date',
        'product',
        'bank_account',
        'receiver_bank_account',
    )

    @admin.display(description='Amount')
    def html_amount(self, obj):
        return format_html(
            format_euro_amount(
                amount_in_cent=obj.balance,
                force_sign=True,
                html=True,
            )
        )

    @admin.display(description='Balance')
    def html_balance(self, obj):
        return format_html(
            format_euro_amount(
                amount_in_cent=obj.balance,
                force_sign=True,
                html=True,
            ),
        )
