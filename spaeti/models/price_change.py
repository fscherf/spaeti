from django.db import models

from spaeti.utils import format_euro_amount


class ProductManager(models.Manager):
    pass


class PriceChange(models.Model):
    objects = ProductManager()

    date = models.DateTimeField()

    issuer = models.ForeignKey(
        'spaeti.Account',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    product = models.ForeignKey(
        'spaeti.Product',
        on_delete=models.CASCADE,
        related_name='price_changes',
    )

    price = models.IntegerField()

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
        price = format_euro_amount(
            amount_in_cent=self.price,
            force_sign=True,
            html=False,
        )

        return f'{self.product} {price}'

    class Meta:
        verbose_name = 'Price Change'
        verbose_name_plural = 'Price Changes'
