from django.db import models

from spaeti import SPAETI_DEFAULT_BANK_ACCOUNT_NAME


class BankAccountManager(models.Manager):
    pass


class BankAccount(models.Model):
    objects = BankAccountManager()

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    account = models.ForeignKey(
        'spaeti.Account',
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=256,
    )

    balance = models.IntegerField(
        editable=False,
        default=0,
    )

    comment = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = ('account', 'name')
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'

    def __str__(self):
        if self.name == SPAETI_DEFAULT_BANK_ACCOUNT_NAME:
            return self.account.username

        return f'{self.account.username} - {self.name}'
