from functools import lru_cache

from lona_picocss.html import Div, H1
from lona import NotFoundError, View
from django.db.models import Q

from spaeti import SPAETI_DEFAULT_BANK_ACCOUNT_NAME, SPAETI_ACCOUNT_USERNAME
from spaeti.models import ProductCategory, BankAccount, Product, Account
from spaeti.components import Breadcrumb, Heading, Actions


class GenericView(View):
    # FIXME: all generic views have to return `lona.html.Div` instead of
    # `lona.html.HTML`, because entry points like `get_extra_head()` wouldn't
    # work then.

    # database helper
    @lru_cache
    def get_product_category(self):
        try:
            return ProductCategory.objects.get(
                slug=self.request.match_info['product_category'],
            )

        except ProductCategory.DoesNotExist:
            raise NotFoundError

    @lru_cache
    def get_product(self):
        try:
            return Product.objects.get(
                slug=self.request.match_info['product'],
            )

        except Product.DoesNotExist:
            raise NotFoundError

    @lru_cache
    def get_account(self):
        try:
            return Account.objects.get(
                username=self.request.match_info['username'],
            )

        except Account.DoesNotExist:
            raise NotFoundError

    @lru_cache
    def get_user_account(self):
        account = Account.objects.filter(
            username=self.request.user.username,
        )

        if account.exists:
            return account.get()

    @lru_cache
    def get_default_bank_account(self):
        bank_account = BankAccount.objects.filter(
            account=self.get_user_account(),
            name=SPAETI_DEFAULT_BANK_ACCOUNT_NAME,
        )

        if bank_account.exists:
            return bank_account.get()

    def get_user_accounts(self):
        return Account.objects.filter(
            ~Q(username=SPAETI_ACCOUNT_USERNAME),
        )

    # HTML entry points
    def get_heading_text(self):
        return []

    def get_actions(self):
        return []

    def get_breadcrumb_entries(self):
        return []

    def get_head(self):
        nodes = [
            Heading(
                H1(self.get_heading_text()),
                Actions(self.get_actions()),
            ),
        ]

        breadcrumb_entries = self.get_breadcrumb_entries()

        if breadcrumb_entries:
            nodes.append(
                Breadcrumb(breadcrumb_entries),
            )

        return nodes

    def get_extra_head(self):
        return []

    def get_body(self):
        return []

    def get_extra_body(self):
        return []

    # event handling
    def handle_request(self, request):
        self.html = Div(
            self.get_head(),
            self.get_extra_head(),
            self.get_body(),
            self.get_extra_body(),
        )

        return self.html
