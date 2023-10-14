from lona_picocss.html import InlineButton, Strong, Modal, H3, P
from lona import RedirectResponse

from spaeti.components import Actions, Action
from spaeti.views.generic import GenericView
from spaeti.forms import ProductRestockForm
from spaeti.database import restock_product
from spaeti.lona_django import DjangoForm


class ProductRestockView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_heading_text(self):
        product = self.get_product()

        return f'Restock "{product.name}"'

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
            'Restock',
        ]

    def handle_save(self, input_event):
        self.modal.close()
        self.show()

        product_category = self.get_product_category()
        product = self.get_product()

        restock_product(
            product=product,
            quantity=self.quantity,
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
            self.quantity = self.form.cleaned_data['quantity']

            self.modal.get_body().nodes = [
                H3('Restocking'),
                P(
                    'Are you sure you want to restock ',
                    Strong(f'{self.quantity} '),
                    f'of "{product.name}"?'
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
            form_class=ProductRestockForm,
            form_data={
                'comment': 'Restock via web interface',
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
                Action('Restock', handle_click=self.open_save_popup),
            ),
            self.modal,
        ]
