from lona_picocss.routes import SETTINGS_ROUTE, DEMO_ROUTES
from lona.routing import MATCH_ALL, Route
from aiohttp_wsgi import WSGIHandler

from spaeti._django.wsgi import application as django_application
from spaeti.utils import debug_is_enabled

django_wsgi_handler = WSGIHandler(django_application)

routes = [

    # home
    Route('/', 'spaeti.views.home.HomeView'),

    # django
    Route(MATCH_ALL, django_wsgi_handler, http_pass_through=True),
]

# lona-picocss debug urls
if debug_is_enabled():
    routes = [
        SETTINGS_ROUTE,
        *DEMO_ROUTES,
        *routes,
    ]
