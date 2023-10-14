from lona import RedirectResponse
from lona.html import P

from spaeti.components import Actions, Action
from spaeti.views.generic import GenericView


class AccountDeleteView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_heading_text(self):
        account = self.get_account()

        return f'Delete "{account.username}"'

    def get_breadcrumb_entries(self):
        account = self.get_account()

        return [
            ('Accounts', self.server.reverse('account__list')),
            (
                account.username,
                self.server.reverse(
                    'account__show',
                    username=account.username,
                ),
            ),
            'Delete',
        ]

    def handle_delete(self, input_event):
        account = self.get_account()
        user = account.get_user()

        account.delete()
        user.delete()

        return RedirectResponse(
            self.server.reverse('account__list'),
        )

    def get_body(self):
        account = self.get_account()

        return [
            P(f'Are you sure you want to delete "{account.username}"?'),
            Actions(
                Action(
                    'Cancel',
                    href=self.server.reverse(
                        'account__show',
                        username=account.username,
                    ),
                    secondary=True,
                ),
                Action('Delete', handle_click=self.handle_delete),
            ),
        ]
