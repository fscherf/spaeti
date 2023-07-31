from django.db import models

from spaeti.utils import format_euro_amount


class BankAccountTransaction(models.Model):
    transaction_id = models.UUIDField()
    date = models.DateTimeField()

    bank_account = models.ForeignKey(
        'spaeti.BankAccount',
        on_delete=models.CASCADE,
        related_name='bank_account',
        blank=True,
        null=True,
    )

    receiver_bank_account = models.ForeignKey(
        'spaeti.BankAccount',
        on_delete=models.CASCADE,
        related_name='receiver_bank_account',
        blank=True,
        null=True,
    )

    amount = models.IntegerField()
    balance = models.IntegerField()

    product = models.ForeignKey(
        'spaeti.Product',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    comment = models.TextField(
        blank=True,
        null=True,
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    def __str__(self):
        amount = format_euro_amount(
            amount_in_cent=self.amount,
            force_sign=True,
            html=False,
        )

        return f'{amount} ({self.bank_account} -> {self.receiver_bank_account})'  # NOQA

    class Meta:
        verbose_name = 'Bank Account Transaction'
        verbose_name_plural = 'Bank Account Transactions'
