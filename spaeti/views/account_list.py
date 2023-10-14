from spaeti.components import AccountTable, Action
from spaeti.views.generic import GenericView


class AccountListView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_breadcrumb_entries(self):
        return [
            ('Accounts', self.server.reverse('account__list')),
        ]

    def get_heading_text(self):
        return 'Accounts'

    def get_actions(self):
        return [
            # TODO: check permission
            Action(
                'Add Account',
                href=self.server.reverse('account__add'),
                icon='plus',
                _id='add',
            ),
        ]

    def get_body(self):
        queryset = self.get_user_accounts().order_by('username')

        return [
            AccountTable(
                queryset=queryset,
                request=self.request,
            )
        ]
