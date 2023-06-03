from django.db import models


class ProductManager(models.Manager):
    pass


class Product(models.Model):
    objects = ProductManager()

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    category = models.ForeignKey(
        'spaeti.ProductCategory',
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=256,
        unique=True,
    )

    price = models.IntegerField()

    barcode = models.TextField(
        blank=True,
        null=True,
    )

    comment = models.TextField(
        blank=True,
        null=True,
    )
