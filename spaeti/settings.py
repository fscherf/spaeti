from lona_picocss.views.error_views import (
    Error500View,
    Error404View,
    Error403View,
)
from lona_picocss import settings as picocss_settings

from spaeti.utils import debug_is_enabled

DEBUG = debug_is_enabled()

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
STATIC_URL_PREFIX = '/static/'

STATIC_DIRS = [
    'static',
    picocss_settings.STATIC_DIR,
]

# middlewares
MIDDLEWARES = [
    'lona_django.middlewares.DjangoSessionMiddleware',
]

# lona-picocss settings
PICOCSS_BRAND = 'Freies Labor - Späti'
PICOCSS_TITLE = 'Späti'
PICOCSS_LOGO = 'logo.svg'
PICOCSS_THEME = 'light'
PICOCSS_COLOR_SCHEME = 'light-green'

PICOCSS_MENU = [
    ['Admin', '/admin/'],
    ['Account', [
        ['Login', '/accounts/login/'],
        ['Logout', '/accounts/logout/'],
    ]],
]
