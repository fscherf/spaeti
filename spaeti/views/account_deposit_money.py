from lona_picocss.html import InlineButton, Strong, Modal, H3, P
from lona import RedirectResponse

from spaeti.components import Actions, Action
from spaeti.views.generic import GenericView
from spaeti.utils import format_euro_amount
from spaeti.lona_django import DjangoForm
from spaeti.forms import DepositMoneyForm
from spaeti.database import deposit_money


class AccountDepositMoneyView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_heading_text(self):
        return 'Deposit Money'

    def get_breadcrumb_entries(self):
        return [
            'Deposit Money',
        ]

    def handle_save(self, input_event):
        self.modal.close()
        self.show()

        deposit_money(
            bank_account=self.get_default_bank_account(),
            amount=self.amount,
            comment='Deposited via web interface',
        )

        return RedirectResponse(self.server.reverse('home'))

    def open_save_popup(self, input_event):
        if not self.form.is_valid():
            return

        with self.html.lock:
            self.amount = self.form.cleaned_data['amount']

            self.modal.get_body().nodes = [
                H3('Deposit Money'),
                P(
                    'Are you sure you want to deposit ',
                    Strong(
                        format_euro_amount(
                            amount_in_cent=self.amount,
                            html=True,
                        ),
                    ),
                    ' ?',
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
        self.form = DjangoForm(
            form_class=DepositMoneyForm,
        )

        self.modal = Modal()

        return [
            self.form,
            Actions(
                Action(
                    'Cancel',
                    href=self.server.reverse('home'),
                    secondary=True,
                ),
                Action('Save', handle_click=self.open_save_popup),
            ),
            self.modal,
        ]
