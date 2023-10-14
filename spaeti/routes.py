from lona_picocss.routes import SETTINGS_ROUTE, DEMO_ROUTES
from lona.routing import MATCH_ALL, Route
from aiohttp_wsgi import WSGIHandler

from spaeti._django.wsgi import application as django_application
from spaeti.utils import debug_is_enabled

django_wsgi_handler = WSGIHandler(django_application)

routes = [

    # accounts
    Route(
        '/accounts/add(/)',
        'spaeti.views.account_add.AccountAddView',
        name='account__add',
    ),

    Route(
        '/accounts/deposit-money(/)',
        'spaeti.views.account_deposit_money.AccountDepositMoneyView',
        name='account__deposit_money',
    ),

    Route(
        '/accounts/<username>/edit(/)',
        'spaeti.views.account_edit.AccountEditView',
        name='account__edit',
    ),

    Route(
        '/accounts/<username>/delete(/)',
        'spaeti.views.account_delete.AccountDeleteView',
        name='account__delete',
    ),

    Route(
        '/accounts/<username>(/)',
        'spaeti.views.account_show.AccountShowView',
        name='account__show',
    ),

    Route(
        '/accounts(/)',
        'spaeti.views.account_list.AccountListView',
        name='account__list',
    ),

    # products (crud)
    Route(
        '/products/<product_category>/add(/)',
        'spaeti.views.product_add.ProductAddView',
        name='product__add',
    ),

    Route(
        '/products/<product_category>/<product>/edit(/)',
        'spaeti.views.product_edit.ProductEditView',
        name='product__edit',
    ),

    Route(
        '/products/<product_category>/<product>/delete(/)',
        'spaeti.views.product_delete.ProductDeleteView',
        name='product__delete',
    ),

    Route(
        '/products/<product_category>/<product>/change-price(/)',
        'spaeti.views.product_change_price.ProductChangePriceView',
        name='product__change_price',
    ),

    Route(
        '/products/<product_category>/<product>(/)',
        'spaeti.views.product_show.ProductShowView',
        name='product__show',
    ),

    Route(
        '/products/<product_category>(/)',
        'spaeti.views.product_list.ProductListView',
        name='product__list',
    ),

    # products
    Route(
        '/products/<product_category>/<product>/buy(/)',
        'spaeti.views.product_buy.ProductBuyView',
        name='product__buy',
    ),

    Route(
        '/products/<product_category>/<product>/restock(/)',
        'spaeti.views.product_restock.ProductRestockView',
        name='product__restock',
    ),

    # home
    Route('/', 'spaeti.views.home.HomeView', name='home'),

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
