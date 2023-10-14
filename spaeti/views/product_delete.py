from lona import RedirectResponse
from lona.html import P

from spaeti.components import Actions, Action
from spaeti.views.generic import GenericView


class ProductDeleteView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_heading_text(self):
        product = self.get_product()

        return f'Delete "{product.name}"'

    def get_breadcrumb_entries(self):
        product_category = self.get_product_category()
        product = self.get_product()

        return [
            ('Products', '#'),
            (
                product_category.name_plural,
                self.server.reverse(
                    'product__list',
                    product_category=product_category.slug,
                ),
            ),
            (
                product.name,
                self.server.reverse(
                    'product__show',
                    product_category=product_category.slug,
                    product=product.slug,
                ),
            ),
            'Delete',
        ]

    def handle_delete(self, input_event):
        product_category = self.get_product_category()
        product = self.get_product()

        product.delete()

        return RedirectResponse(
            self.server.reverse(
                'product__list',
                product_category=product_category.slug,
            ),
        )

    def get_body(self):
        product_category = self.get_product_category()
        product = self.get_product()

        return [
            P(f'Are you sure you want to delete "{product.name}"?'),
            Actions(
                Action(
                    'Cancel',
                    href=self.server.reverse(
                        'product__show',
                        product_category=product_category.slug,
                        product=product.slug,
                    ),
                    secondary=True,
                ),
                Action('Delete', handle_click=self.handle_delete),
            ),
        ]
