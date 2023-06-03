from django.db import models


class ProductCategory(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    name = models.CharField(
        max_length=256,
    )

    comment = models.TextField(
        blank=True,
        null=True,
    )
