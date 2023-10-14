from lona import RedirectResponse
from lona.html import Strong, P

from spaeti.components import Actions, Action
from spaeti.views.generic import GenericView
from spaeti.utils import format_euro_amount
from spaeti.database import buy_product


class ProductBuyView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_heading_text(self):
        product = self.get_product()

        return f'Buy "{product.name}"'

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
            'Buy',
        ]

    def handle_buy(self, input_event):
        product_category = self.get_product_category()
        product = self.get_product()

        buy_product(
            bank_account=self.get_default_bank_account(),
            product=product,
            comment='Bought via web interface',
        )

        return RedirectResponse(
            self.server.reverse(
                'product__show',
                product_category=product_category.slug,
                product=product.slug,
            ),
        )

    def get_body(self):
        product_category = self.get_product_category()
        product = self.get_product()

        return [
            P(
                'Are you sure you want to buy a ',
                Strong(f'{product.name} '),
                'for ',
                Strong(
                    format_euro_amount(
                        amount_in_cent=product.price,
                        html=True,
                    ),
                ),
                '?',
            ),

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
                Action('Buy', handle_click=self.handle_buy),
            ),
        ]
