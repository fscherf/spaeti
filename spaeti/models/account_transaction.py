from django.db import models


class AccountTransaction(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    date = models.DateTimeField()

    sender_account = models.ForeignKey(
        'spaeti.Account',
        on_delete=models.CASCADE,
        related_name='sender_account',
    )

    receiver_account = models.ForeignKey(
        'spaeti.Account',
        on_delete=models.CASCADE,
        related_name='receiver_account',
    )

    amount = models.IntegerField()

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

    class Meta:
        verbose_name = 'Account Transaction'
        verbose_name_plural = 'Account Transactions'

    def __str__(self):
        return f'{self.amount} ({self.sender_account} -> {self.receiver_account})'  # NOQA
