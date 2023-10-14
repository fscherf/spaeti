from lona import RedirectResponse

from spaeti.components import QRCodeScanner, Actions, Spacer, Action
from spaeti.views.generic import GenericView
from spaeti.lona_django import DjangoForm
from spaeti.forms import ProductEditForm


class ProductEditView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_heading_text(self):
        product = self.get_product()

        return f'Edit "{product.name}"'

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
            'Edit',
        ]

    def handle_save(self, input_event):
        product_category = self.get_product_category()
        product = self.get_product()

        if not self.form.is_valid():
            return

        self.form.save()

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
        product = self.get_product()

        self.form = DjangoForm(
            form_class=ProductEditForm,
            instance=product,
        )

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
                        'product__show',
                        product_category=product_category.slug,
                        product=product.slug,
                    ),
                    secondary=True,
                ),
                Action('Save', handle_click=self.handle_save),
            ),
            scanner,
        ]
