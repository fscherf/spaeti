from django.db import models


class Person(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    username = models.CharField(
        max_length=256,
        unique=True,
    )

    comment = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.username
