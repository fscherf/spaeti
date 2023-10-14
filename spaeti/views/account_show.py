from spaeti.components import AccountAttributeTable, Action
from spaeti.views.generic import GenericView


class AccountShowView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_breadcrumb_entries(self):
        account = self.get_account()

        return [
            ('Accounts', self.server.reverse('account__list')),
            account.username,
        ]

    def get_heading_text(self):
        return self.get_account().username

    def get_actions(self):
        account = self.get_account()

        return [
            Action(
                'Edit',
                href=self.server.reverse(
                    'account__edit',
                    username=account.username,
                ),
                icon='edit',
                _id='edit',
            ),
            Action(
                'Delete',
                href=self.server.reverse(
                    'account__delete',
                    username=account.username,
                ),
                icon='trash-2',
                _id='delete',
            ),
        ]

    def get_body(self):
        return [
            AccountAttributeTable(
                instance=self.get_account(),
            ),
        ]
