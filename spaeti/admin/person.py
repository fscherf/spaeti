from django.contrib import admin

from spaeti.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass
