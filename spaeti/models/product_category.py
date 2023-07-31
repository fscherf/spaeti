from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
    )

    name_plural = models.CharField(
        max_length=256,
        unique=True,
    )

    slug = models.CharField(
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
