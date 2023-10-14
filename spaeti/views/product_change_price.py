from lona_picocss.html import InlineButton, Strong, Modal, H3, P
from lona import RedirectResponse

from spaeti.database import change_product_price
from spaeti.forms import ProductChangePriceForm
from spaeti.components import Actions, Action
from spaeti.views.generic import GenericView
from spaeti.utils import format_euro_amount
from spaeti.lona_django import DjangoForm


class ProductChangePriceView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_heading_text(self):
        product = self.get_product()

        return f'Change Price of "{product.name}"'

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
            'Change Price',
        ]

    def handle_save(self, input_event):
        self.modal.close()
        self.show()

        product_category = self.get_product_category()
        product = self.get_product()

        change_product_price(
            product=product,
            price=self.price,
            issuer=self.get_user_account(),
            comment=self.form.cleaned_data['comment'],
        )

        return RedirectResponse(
            self.server.reverse(
                'product__show',
                product_category=product_category.slug,
                product=product.slug,
            ),
        )

    def open_save_popup(self, input_event):
        if not self.form.is_valid():
            return

        product = self.get_product()

        with self.html.lock:
            self.price = self.form.cleaned_data['price']

            self.modal.get_body().nodes = [
                H3('Change Price'),
                P(
                    'Are you sure you want to change the price of ',
                    Strong(f'{product.name} '),
                    'to ',
                    Strong(
                        format_euro_amount(
                            amount_in_cent=self.price,
                            html=True,
                        ),
                    ),
                    '?',
                ),
            ]

            self.modal.get_footer().nodes = [
                InlineButton(
                    'Cancel',
                    handle_click=lambda i: self.modal.close(),
                    secondary=True,
                ),
                InlineButton(
                    'OK',
                    handle_click=self.handle_save,
                )
            ]

            self.modal.open()

    def get_body(self):
        product_category = self.get_product_category()
        product = self.get_product()

        self.form = DjangoForm(
            form_class=ProductChangePriceForm,
            form_data={
                'comment': 'Price changed via web interface',
            },
        )

        self.modal = Modal()

        return [
            self.form,
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
                Action('Change', handle_click=self.open_save_popup),
            ),
            self.modal,
        ]
