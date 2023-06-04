from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db import transaction

from spaeti.models import (
    ProductTransaction,
    AccountTransaction,
    ProductCategory,
    Product,
    Account,
    Person,
)

SPAETI_PERSON_USERNAME = 'spaeti'
DEFAULT_ACCOUNT_NAME = 'default'


@transaction.atomic
def get_spaeti_account():
    spaeti, _ = Person.objects.get_or_create(
        username=SPAETI_PERSON_USERNAME,
    )

    spaeti_account, _ = Account.objects.get_or_create(
        person=spaeti,
        name=DEFAULT_ACCOUNT_NAME,
    )

    return spaeti_account


def username_is_available(username):
    return Person.objects.filter(username=username).exists()


@transaction.atomic
def add_account(username, email, login=True):
    if login:
        User = get_user_model()

        User.objects.create(
            username=username,
            email=email,
        )

    person = Person.objects.create(
        username=username,
    )

    Account.objects.create(
        person=person,
        name=DEFAULT_ACCOUNT_NAME,
    )

    return person


def add_product_category(name):
    return ProductCategory.objects.create(name=name)


@transaction.atomic
def add_product(category, name, price):
    return Product.objects.create(
        category=category,
        name=name,
        price=price,
    )


@transaction.atomic
def restock_product(issuer, product, quatity, date=None):
    date = date or now()

    return ProductTransaction.objects.create(
        issuer=issuer,
        product=product,
        quatity=date,
    )


@transaction.atomic
def buy_product(account, product, date=None):
    date = date or now()
    spaeti_account = get_spaeti_account()

    account_transaction = AccountTransaction.objects.create(
        date=date,
        product=product,
        sender_account=account,
        receiver_account=spaeti_account,
        amount=product.price,
    )

    product_transaction = ProductTransaction.objects.create(
        date=date,
        issuer=account.person,
        product=product,
        quatity=-1,
    )

    return account_transaction, product_transaction


@transaction.atomic
def send_money(sender_account, receiver_account, amount, date=None):
    date = date or now()

    return AccountTransaction.objects.create(
        date=date,
        product=None,
        sender_account=sender_account,
        receiver_account=receiver_account,
        amount=amount,
    )


@transaction.atomic
def deposit_money(account, amount, date=None):
    spaeti_account = get_spaeti_account()

    cash_transaction = AccountTransaction.objects.create(
        date=date,
        product=None,
        sender_account=account,
        receiver_account=spaeti_account,
        amount=amount,
    )

    deposit_transaction = AccountTransaction.objects.create(
        date=date,
        product=None,
        sender_account=account,
        receiver_account=account,
        amount=amount,
    )

    return cash_transaction, deposit_transaction
