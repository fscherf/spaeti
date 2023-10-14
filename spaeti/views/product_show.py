from lona_picocss.html import H2

from spaeti.components import (
    ProductTransactionTable,
    ProductPriceChangeTable,
    ProductAttributeTable,
    Spacer,
    Action,
)
from spaeti.models import ProductTransaction, PriceChange
from spaeti.views.generic import GenericView


class ProductShowView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_breadcrumb_entries(self):
        product_category = self.get_product_category()
        product = self.get_product()

        return [
            ('Products', '#'),  # FIXME
            (
                product_category.name_plural,
                self.server.reverse(
                    'product__list',
                    product_category=product_category.slug,
                ),
            ),
            product.name,
        ]

    def get_heading_text(self):
        return self.get_product().name

    def get_actions(self):
        product_category = self.get_product_category()
        product = self.get_product()

        return [
            Action(
                'Edit',
                href=self.server.reverse(
                    'product__edit',
                    product_category=product_category.slug,
                    product=product.slug,
                ),
                icon='edit',
                _id='edit',
            ),
            Action(
                'Delete',
                href=self.server.reverse(
                    'product__delete',
                    product_category=product_category.slug,
                    product=product.slug,
                ),
                icon='trash-2',
                _id='delete',
            ),
            Action(
                'Restock',
                href=self.server.reverse(
                    'product__restock',
                    product_category=product_category.slug,
                    product=product.slug,
                ),
                icon='plus',
                _id='restock',
            ),
            Action(
                'Change Price',
                href=self.server.reverse(
                    'product__change_price',
                    product_category=product_category.slug,
                    product=product.slug,
                ),
                icon='edit',
                _id='change-price',
            ),
            Spacer(),
            Action(
                'Buy',
                href=self.server.reverse(
                    'product__buy',
                    product_category=product_category.slug,
                    product=product.slug,
                ),
                icon='shopping-cart',
                _id='buy',
            ),
        ]

    def get_body(self):
        product = self.get_product()

        product_transactions = ProductTransaction.objects.filter(
            product=product,
        ).order_by(
            '-date',
        )

        price_changes = PriceChange.objects.filter(
            product=product,
        ).order_by(
            '-date',
        )

        return [
            ProductAttributeTable(
                instance=self.get_product(),
            ),

            H2('Restockings'),
            ProductTransactionTable(
                queryset=product_transactions,
            ),

            H2('Price Changes'),
            ProductPriceChangeTable(
                queryset=price_changes,
            ),
        ]
