from spaeti.components import ProductTable, Action
from spaeti.views.generic import GenericView
from spaeti.models import Product


class ProductListView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_breadcrumb_entries(self):
        product_category = self.get_product_category()

        return [
            ('Products', '#'),  # FIXME
            product_category.name_plural,
        ]

    def get_heading_text(self):
        return self.get_product_category().name_plural

    def get_actions(self):
        product_category = self.get_product_category()

        return [
            # TODO: check permission
            Action(
                f'Add {product_category.name}',
                href=self.server.reverse(
                    'product__add',
                    product_category=product_category.slug,
                ),
                icon='plus',
                _id='add',
            ),
        ]

    def get_body(self):
        queryset = Product.objects.filter(
            category=self.get_product_category(),
        ).order_by(
            'name',
        )

        return [
            ProductTable(
                queryset=queryset,
                request=self.request,
            )
        ]
