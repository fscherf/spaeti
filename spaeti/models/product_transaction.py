from django.db import models


class ProductTransaction(models.Model):
    transaction_id = models.UUIDField()
    date = models.DateTimeField()

    issuer = models.ForeignKey(
        'spaeti.Account',
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        'spaeti.Product',
        on_delete=models.CASCADE,
    )

    quantity = models.IntegerField()

    stock = models.IntegerField()

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

    class Meta:
        verbose_name = 'Product Transaction'
        verbose_name_plural = 'Product Transactions'

    def __str__(self):
        return f'{self.product} +{self.quantity}'
