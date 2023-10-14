from lona import RedirectResponse

from spaeti.components import QRCodeScanner, Actions, Spacer, Action
from spaeti.views.generic import GenericView
from spaeti.lona_django import DjangoForm
from spaeti.forms import ProductAddForm
from spaeti.database import add_product


class ProductAddView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_heading_text(self):
        product_category = self.get_product_category()

        return f'Add {product_category.name}'

    def get_breadcrumb_entries(self):
        product_category = self.get_product_category()

        return [
            ('Products', '#'),  # FIXME
            (
                product_category.name_plural,
                self.server.reverse(
                    'product__list',
                    product_category=product_category.slug,
                ),
            ),
            'Add',
        ]

    def handle_save(self, input_event):
        if not self.form.is_valid():
            return

        product_category = self.get_product_category()
        product = add_product(**self.form.cleaned_data)

        return RedirectResponse(
            self.server.reverse(
                'product__show',
                product_category=product_category.slug,
                product=product.slug,
            ),
        )

    def handle_scan_result(self, scanner, data):
        self.form.set_value('barcode', data['decodedText'])

    def get_body(self):
        product_category = self.get_product_category()
        self.form = DjangoForm(form_class=ProductAddForm)

        scanner = QRCodeScanner(
            handle_scan_result=self.handle_scan_result,
        )

        return [
            self.form,
            Actions(
                Action(
                    'Scan Barcode',
                    handle_click=lambda i: scanner.start_scanning(),
                    secondary=True,
                ),
                Spacer(),
                Action(
                    'Cancel',
                    href=self.server.reverse(
                        'product__list',
                        product_category=product_category.slug,
                    ),
                    secondary=True,
                ),
                Action('Save', handle_click=self.handle_save),
            ),
            scanner,
        ]
