from aiohttp_wsgi import WSGIHandler
from lona.routing import Route

from spaeti._django.wsgi import application as django_application

django_wsgi_handler = WSGIHandler(django_application)


routes = [
    Route('/admin/<path:.*>', django_wsgi_handler, http_pass_through=True),

    # home
    Route('/', 'spaeti.views.home.HomeView'),
]