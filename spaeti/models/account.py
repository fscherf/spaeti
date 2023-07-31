from functools import lru_cache

from django.contrib.auth import get_user_model
from django.db import models

from spaeti import SPAETI_DEFAULT_BANK_ACCOUNT_NAME


class Account(models.Model):
    username = models.CharField(
        max_length=256,
        unique=True,
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

    @lru_cache
    def get_default_bank_account(self):
        return self.bankaccount_set.get(
            name=SPAETI_DEFAULT_BANK_ACCOUNT_NAME,
        )

    def get_user(self):
        user = get_user_model().objects.filter(username=self.username)

        if user.exists():
            return user.get()

    def get_flags(self):
        flags = set()
        user = self.get_user()

        if user:
            if user.is_active:
                flags.add('login')

            if user.is_staff:
                flags.add('django-staff')

            if user.is_superuser:
                flags.add('django-superuser')

            for group in user.groups.filter(name__startswith='spaeti-'):
                flags.add(group.name)

        return sorted(list(flags))

    def __str__(self):
        return self.username
