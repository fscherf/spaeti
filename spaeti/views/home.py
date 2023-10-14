from lona_picocss.html import InlineButton, Strong, Modal, H3, H2, P
from lona import RedirectResponse
from django.db.models import Q

from spaeti.components import (
    BankAccountTransactionTable,
    QRCodeScanner,
    Action,
)
from spaeti.models import BankAccountTransaction, Product
from spaeti.views.generic import GenericView
from spaeti.utils import format_euro_amount


class HomeView(GenericView):
    def get_heading_text(self):
        return 'Späti'

    def get_breadcrumb_entries(self):
        return ['Dashboard']

    def get_actions(self):
        return [
            Action(
                'Deposit Money',
                href=self.server.reverse('account__deposit_money'),
                icon='dollar-sign',
                _id='deposit-money',
            ),
            Action(
                'Scan',
                handle_click=lambda i: self.scanner.start_scanning(),
                icon='search',
                _id='scan',
            ),
        ]

    def handle_scan_result(self, scanner, data):
        self.show()  # close modal

        barcode = data['decodedText']
        product = Product.objects.filter(barcode=barcode)

        if not product.exists():
            self.modal.get_body().nodes = [
                H3('Unknown Barcode'),
                P(f'No product with barcode "{barcode}" found'),
            ]

            self.modal.get_footer().nodes = [
                InlineButton(
                    'OK',
                    handle_click=lambda i: self.modal.close(),
                )
            ]

            self.modal.open()

            return

        product = product.get()

        return RedirectResponse(
            self.server.reverse(
                'product__show',
                product_category=product.category.slug,
                product=product.slug,
            ),
        )

    def get_body(self):
        if not self.request.user.is_authenticated:
            return [
                P(
                    Strong('Welcome to Späti! '),
                    'Späti is a Pre Paid system for drinks at Freies Labor.',
                ),
                P(
                    'You are currently not logged in. '
                    'You need an account and be logged '
                    'in in order to buy drinks.',
                ),
            ]

        account = self.get_user_account()
        bank_account = self.get_default_bank_account()

        self.scanner = QRCodeScanner(
            handle_scan_result=self.handle_scan_result,
        )

        bank_account_transactions_table = BankAccountTransactionTable(
            queryset=BankAccountTransaction.objects.filter(
                Q(bank_account=bank_account),
                ~Q(receiver_bank_account=bank_account),
            ).order_by(
                '-date',
            ),
        )

        self.modal = Modal()

        return [
            P(
                f'Hello {account.username}! Your balance is ',
                Strong(
                    format_euro_amount(
                        amount_in_cent=bank_account.balance,
                        html=True,
                    ),
                ),
            ),

            H2('Transactions'),
            bank_account_transactions_table,

            self.scanner,
            self.modal,
        ]
