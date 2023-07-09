import os

from lona_picocss import (
    get_django_show_exceptions,
    get_django_auth_navigation,
    get_debug_navigation,
    Error500View,
    Error404View,
    Error403View,
)
from lona_picocss import settings as picocss_settings

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
    'lona_django.middlewares.DjangoSessionMiddleware',
]

# lona-picocss settings
PICOCSS_BRAND = 'Freies Labor - Späti'
PICOCSS_TITLE = 'Späti'
PICOCSS_LOGO = 'logo.svg'
PICOCSS_THEME = 'light'
PICOCSS_COLOR_SCHEME = 'light-green'


def get_navigation(server, request):
    nav_items = []

    # lona-picocss debug
    if debug_is_enabled and request.user.is_staff:
        nav_items.extend(get_debug_navigation(server, request))

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
