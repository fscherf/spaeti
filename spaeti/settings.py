import os

from lona_picocss import (
    get_django_show_exceptions,
    get_django_auth_navigation,
    Error500View,
    Error404View,
    Error403View,
)
from lona_picocss import settings as picocss_settings
from lona_picocss import NavItem

from spaeti.utils import test_suite_is_running, debug_is_enabled

DEBUG = debug_is_enabled()
TEST_SUITE_IS_RUNNING = test_suite_is_running()

# feature flags
STOP_DAEMON_WHEN_VIEW_FINISHES = False
CLIENT_VERSION = 2
USE_FUTURE_NODE_CLASSES = True

# routing
ROUTING_TABLE = 'routes.py::routes'

# templating
TEMPLATE_DIRS = [
    picocss_settings.TEMPLATE_DIR,
]

FRONTEND_TEMPLATE = picocss_settings.FRONTEND_TEMPLATE
FRONTEND_TEMPLATE = picocss_settings.FRONTEND_TEMPLATE
ERROR_403_VIEW = Error403View
ERROR_404_VIEW = Error404View
ERROR_500_VIEW = Error500View

# static files
STATIC_FILES_SERVE = TEST_SUITE_IS_RUNNING
STATIC_URL_PREFIX = '/static/'

STATIC_DIRS = [
    'static',
    picocss_settings.STATIC_DIR,
]

# middlewares
MIDDLEWARES = [
    'lona_picocss.middlewares.LonaPicocssMiddleware',
    'spaeti.lona_django.middlewares.DjangoSessionMiddleware',
]

# lona-picocss settings
PICOCSS_BRAND = 'Freies Labor - Späti'
PICOCSS_TITLE = 'Späti'
PICOCSS_LOGO = 'logo.svg'
PICOCSS_THEME = 'light'
PICOCSS_COLOR_SCHEME = 'light-green'


def get_navigation(server, request):
    from spaeti.models import ProductCategory

    nav_items = []

    def is_member(group_name):
        if request.user.is_superuser:
            return True

        return request.user.groups.filter(name=group_name).exists()

    def get_product_categories():
        return ProductCategory.objects.order_by('name_plural')

    menu = NavItem(
        title='Menu',
    )

    # accounts
    if is_member('spaeti-admin'):
        menu.nav_items.append(
            NavItem(
                title='Accounts',
                url=server.reverse('account__list'),
            ),
        )

    # products
    if request.user.is_authenticated:
        for product_category in get_product_categories():
            menu.nav_items.append(
                NavItem(
                    title=product_category.name_plural,
                    url=server.reverse(
                        'product__list',
                        product_category=product_category.slug,
                    ),
                ),
            )

    if menu.nav_items:
        nav_items.append(menu)

    # django auth
    nav_items.extend(get_django_auth_navigation(server, request))

    return nav_items


PICOCSS_NAVIGATION = get_navigation
PICOCSS_SHOW_EXCEPTIONS = get_django_show_exceptions

# client
CLIENT_PING_INTERVAL = 30  # nginx proxy_read_timeout is set to 60s by default

# threads
MAX_WORKER_THREADS = int(os.environ.get('SPAETI_MAX_WORKER_THREADS', '4'))
MAX_RUNTIME_THREADS = int(os.environ.get('SPAETI_MAX_RUNTIME_THREADS', '6'))
