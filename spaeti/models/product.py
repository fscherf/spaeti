from django.db import models


class Product(models.Model):
    category = models.ForeignKey(
        'spaeti.ProductCategory',
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=256,
        unique=True,
    )

    slug = models.CharField(
        max_length=256,
        unique=True,
    )

    price = models.IntegerField(
        help_text='Prices are saved in cents',
    )

    stock = models.IntegerField(default=0)

    barcode = models.CharField(
        max_length=256,
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
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
