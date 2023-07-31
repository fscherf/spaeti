import logging

from django.apps import AppConfig

logger = logging.getLogger('spaeti')


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spaeti'
    verbose_name = 'Spaeti'

    def ready(self):
        from django.contrib.auth.models import Group

        from spaeti.database import (
            get_spaeti_bank_account,
            get_default_category,
        )

        # create spaeti internal categories, accounts, and groups
        try:
            get_spaeti_bank_account()
            get_default_category()

            Group.objects.get_or_create(name='spaeti-staff')
            Group.objects.get_or_create(name='spaeti-admin')

        except Exception:
            logger.warning('could not get or create default database entries')
