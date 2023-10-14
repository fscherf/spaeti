from lona import RedirectResponse

from spaeti.components import Actions, Action
from spaeti.views.generic import GenericView
from spaeti.database import update_account
from spaeti.lona_django import DjangoForm
from spaeti.forms import AccountEditForm


class AccountEditView(GenericView):
    DJANGO_AUTH_GROUPS_REQUIRED = ['spaeti-admin']

    def get_heading_text(self):
        account = self.get_account()

        return f'Edit "{account.username}"'

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
            'Edit',
        ]

    def handle_save(self, input_event):
        if not self.form.is_valid():
            return

        account = self.get_account()

        update_account(
            username=account.username,
            email=self.form.cleaned_data['email'],
            login=self.form.cleaned_data['login'],
            spaeti_staff=self.form.cleaned_data['spaeti_staff'],
            spaeti_admin=self.form.cleaned_data['spaeti_admin'],
            django_staff=self.form.cleaned_data['django_staff'],
            django_superuser=self.form.cleaned_data['django_superuser'],
        )

        return RedirectResponse(
            self.server.reverse(
                'account__show',
                username=account.username,
            )
        )

    def get_body(self):
        account = self.get_account()
        user = account.get_user()
        group_names = user.groups.values_list('name', flat=True)

        self.form = DjangoForm(
            form_class=AccountEditForm,
            form_data={
                'email': user.email,
                'login': user.is_active,
                'spaeti_staff': 'spaeti-staff' in group_names,
                'spaeti_admin': 'spaeti-admin' in group_names,
                'django_staff': user.is_staff,
                'django_superuser': user.is_superuser,
                'comment': account.comment,
            },
        )

        return [
            self.form,
            Actions(
                Action(
                    'Cancel',
                    href=self.server.reverse(
                        'account__show',
                        username=account.username,
                    ),
                    secondary=True,
                ),
                Action('Save', handle_click=self.handle_save),
            ),
        ]
