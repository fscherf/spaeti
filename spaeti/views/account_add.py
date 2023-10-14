from lona import RedirectResponse

from spaeti.components import Actions, Action
from spaeti.views.generic import GenericView
from spaeti.lona_django import DjangoForm
from spaeti.forms import AccountAddForm
from spaeti.database import add_account


class AccountAddView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_heading_text(self):
        return 'Add Account'

    def get_breadcrumb_entries(self):
        return [
            ('Accounts', self.server.reverse('account__list')),
            'Add',
        ]

    def handle_save(self, input_event):
        if not self.form.is_valid():
            return

        account = add_account(
            username=self.form.cleaned_data['username'],
            email=self.form.cleaned_data['email'],
            comment=self.form.cleaned_data['comment'],
            login=self.form.cleaned_data['login'],
            spaeti_staff=self.form.cleaned_data['spaeti_staff'],
            spaeti_admin=self.form.cleaned_data['spaeti_admin'],
            django_staff=self.form.cleaned_data['django_staff'],
            django_superuser=self.form.cleaned_data['django_superuser'],
        )

        return RedirectResponse(
            self.server.reverse('account__show', username=account.username),
        )

    def get_body(self):
        self.form = DjangoForm(form_class=AccountAddForm)

        return [
            self.form,
            Actions(
                Action(
                    'Cancel',
                    href=self.server.reverse('account__list'),
                    secondary=True,
                ),
                Action('Save', handle_click=self.handle_save),
            ),
        ]
