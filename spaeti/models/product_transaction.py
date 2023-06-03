from django.db import models


class ProductTransaction(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    date = models.DateTimeField()

    issuer = models.ForeignKey(
        'spaeti.Person',
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        'spaeti.Product',
        on_delete=models.CASCADE,
    )

    quantity = models.IntegerField()

    comment = models.TextField(
        blank=True,
        null=True,
    )
