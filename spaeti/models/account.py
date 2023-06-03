from django.db import models


class AccountManager(models.Manager):
    pass


class Account(models.Model):
    objects = AccountManager()

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    person = models.ForeignKey(
        'spaeti.Person',
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=256,
    )

    balance_cache = models.IntegerField(
        editable=False,
        default=0,
    )

    balance_cache_timestamp = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    comment = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = ('person', 'name')
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return f'{self.person.username} - {self.name}'
