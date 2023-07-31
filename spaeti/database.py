from datetime import datetime
from uuid import uuid1

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.timezone import now
from django.utils import timezone
from django.db import transaction
from slugify import slugify

from spaeti import (
    SPAETI_DEFAULT_PRODUCT_CATEGORY_NAME_PLURAL,
    SPAETI_DEFAULT_PRODUCT_CATEGORY_SLUG,
    SPAETI_DEFAULT_PRODUCT_CATEGORY_NAME,
    SPAETI_DEFAULT_BANK_ACCOUNT_NAME,
    SPAETI_ACCOUNT_USERNAME,
)
from spaeti.models import (
    BankAccountTransaction,
    ProductTransaction,
    ProductCategory,
    PriceChange,
    BankAccount,
    Product,
    Account,
)


@transaction.atomic
def get_spaeti_bank_account() -> BankAccount:
    spaeti_account, _ = Account.objects.get_or_create(
        username=SPAETI_ACCOUNT_USERNAME,
    )

    spaeti_bank_account, _ = BankAccount.objects.get_or_create(
        account=spaeti_account,
        name=SPAETI_DEFAULT_BANK_ACCOUNT_NAME,
    )

    return spaeti_bank_account


def email_is_available(email: str) -> bool:
    User = get_user_model()

    return not User.objects.filter(email=email).exists()


def username_is_available(username: str) -> bool:
    User = get_user_model()

    return not User.objects.filter(username=username).exists()


@transaction.atomic
def add_account(
        username: str,
        email: str = '',
        login: bool = True,
        spaeti_staff: bool = False,
        spaeti_admin: bool = False,
        django_staff: bool = False,
        django_superuser: bool = False,
        comment: str = '',
) -> Account:

    User = get_user_model()

    user, created = User.objects.get_or_create(
        username=username,
        email=email,
    )

    account = Account.objects.create(
        username=username,
        comment=comment,
    )

    BankAccount.objects.create(
        account=account,
        name=SPAETI_DEFAULT_BANK_ACCOUNT_NAME,
    )

    # django user flags
    user.is_active = login
    user.is_staff = django_staff
    user.is_superuser = django_superuser

    # django groups
    if spaeti_staff:
        Group.objects.get(name='spaeti-staff').user_set.add(user)

    if spaeti_admin:
        Group.objects.get(name='spaeti-admin').user_set.add(user)

    user.save()

    return account


@transaction.atomic
def update_account(
        username: str,
        email: str | None = None,
        login: bool | None = None,
        spaeti_staff: bool | None = None,
        spaeti_admin: bool | None = None,
        django_staff: bool | None = None,
        django_superuser: bool | None = None,
        comment: str | None = None,
) -> Account:

    # TODO: destroy running sessions

    account = Account.objects.get(username=username)
    user = account.get_user()

    # account fields
    if comment is not None:
        account.comment = comment

    # django user fields
    if email is not None:
        user.email = email

    if login is not None:
        user.is_active = login

    if django_staff is not None:
        user.is_staff = django_staff

    if django_superuser is not None:
        user.is_superuser = django_superuser

    # django groups
    if spaeti_staff is not None:
        group = Group.objects.get(name='spaeti-staff')

        if spaeti_staff:
            group.user_set.add(user)

        else:
            group.user_set.remove(user)

    if spaeti_admin is not None:
        group = Group.objects.get(name='spaeti-admin')

        if spaeti_admin:
            group.user_set.add(user)

        else:
            group.user_set.remove(user)

    account.save()
    user.save()

    return account


@transaction.atomic
def add_product_category(
        name: str,
        name_plural: str,
        slug: str = '',
) -> ProductCategory:

    if not slug:
        slug = slugify(name_plural)

    return ProductCategory.objects.create(
        name=name,
        name_plural=name_plural,
        slug=slug,
    )


def get_default_category() -> ProductCategory:
    product_category, _ = ProductCategory.objects.get_or_create(
        name_plural=SPAETI_DEFAULT_PRODUCT_CATEGORY_NAME_PLURAL,
        name=SPAETI_DEFAULT_PRODUCT_CATEGORY_NAME,
        slug=SPAETI_DEFAULT_PRODUCT_CATEGORY_SLUG,
    )

    return product_category


@transaction.atomic
def add_product(
        name: str,
        price: int,
        stock: int = 0,
        category: ProductCategory | None = None,
        barcode: str = '',
        comment: str = '',
        slug: str = '',
) -> Product:

    if not slug:
        slug = slugify(name)

    category = category or get_default_category()

    product = Product.objects.create(
        category=category,
        name=name,
        price=price,
        stock=stock,
        barcode=barcode,
        comment=comment,
        slug=slug,
    )

    PriceChange.objects.create(
        product=product,
        price=price,
        date=timezone.now(),
        comment='Initial price',
    )

    return product


@transaction.atomic
def restock_product(
        product: Product,
        quantity: int,
        date: datetime | None = None,
        issuer: Account | None = None,
        comment: str = '',
) -> uuid1:

    date = date or now()
    issuer = issuer or get_spaeti_bank_account().account
    transaction_id = uuid1()

    # update product stock
    product.stock += quantity

    product.save()

    # generate product transaction
    ProductTransaction.objects.create(
        product=product,
        issuer=issuer,
        quantity=quantity,
        stock=product.stock,
        transaction_id=transaction_id,
        date=date,
        comment=comment,
    )

    return transaction_id


@transaction.atomic
def deposit_money(
        bank_account: BankAccount,
        amount: int,
        date: datetime | None = None,
        comment: str = '',
) -> uuid1:

    date = date or now()
    spaeti_bank_account = get_spaeti_bank_account()
    transaction_id = uuid1()

    # update account balance
    bank_account.balance += amount

    bank_account.save()

    # update spaeti account balance
    spaeti_bank_account.balance += amount

    spaeti_bank_account.save()

    # account -> spaeti-account transaction
    BankAccountTransaction.objects.create(
        bank_account=bank_account,
        receiver_bank_account=spaeti_bank_account,
        amount=amount,
        balance=bank_account.balance,
        transaction_id=transaction_id,
        date=date,
        comment=comment,
    )

    # account -> account transaction
    BankAccountTransaction.objects.create(
        bank_account=bank_account,
        receiver_bank_account=bank_account,
        amount=amount,
        balance=bank_account.balance,
        transaction_id=transaction_id,
        date=date,
        comment=comment,
    )

    return transaction_id


@transaction.atomic
def transfer_money(
        bank_account: BankAccount,
        amount: int,
        receiver_bank_account: BankAccount | None = None,
        date: datetime | None = None,
        comment: str = '',
) -> uuid1:

    # FIXME: check if transaction_id is already in use

    date = date or now()
    transaction_id = uuid1()

    # update account balance
    bank_account.balance += (amount * -1)
    bank_account.save()

    # update receiver_account balance
    if receiver_bank_account:
        receiver_bank_account.balance += amount
        receiver_bank_account.save()

    # create account transaction for the sending account
    BankAccountTransaction.objects.create(
        account=bank_account,
        receiver_account=receiver_bank_account,
        amount=amount * -1,
        balance=bank_account.balance,
        transaction_id=transaction_id,
        date=date,
        comment=comment,
    )

    # create account transaction for the receiver_account
    if receiver_bank_account:
        BankAccountTransaction.objects.create(
            account=receiver_bank_account,
            receiver_account=bank_account,
            amount=amount,
            balance=receiver_bank_account.balance,
            transaction_id=transaction_id,
            date=date,
            comment=comment,
        )

    return transaction_id


@transaction.atomic
def transfer_money_to_spaeti_account(
        amount: int,
        date: datetime | None = None,
        comment: str = '',
) -> uuid1:

    # FIXME: check if transaction_id is already in use

    date = date or now()
    transaction_id = uuid1()
    spaeti_bank_account = get_spaeti_bank_account()

    # update account balance
    spaeti_bank_account.balance += amount
    spaeti_bank_account.save()

    # create bank account transaction
    BankAccountTransaction.objects.create(
        account=spaeti_bank_account,
        receiver_account=None,
        amount=amount,
        balance=spaeti_bank_account.balance,
        transaction_id=transaction_id,
        date=date,
        comment=comment,
    )

    return transaction_id


@transaction.atomic
def buy_product(
        bank_account: BankAccount,
        product: Product,
        date: datetime | None = None,
        comment: str = '',
) -> uuid1:

    # FIXME: check if transaction_id is already in use
    # TODO: implement ProductNotInstockException
    # TODO: implement BalanceInsuficientException

    date = date or now()
    spaeti_account = get_spaeti_bank_account()
    transaction_id = uuid1()

    # run checks
    if product.stock < 1:
        raise RuntimeError('product is not in stock')

    # decrease bank account balance
    bank_account.balance -= product.price

    bank_account.save()

    # decrease product stock
    product.stock -= 1

    product.save()

    # create account transaction
    BankAccountTransaction.objects.create(
        product=product,
        bank_account=bank_account,
        receiver_bank_account=spaeti_account,
        amount=product.price * -1,
        balance=bank_account.balance,
        transaction_id=transaction_id,
        date=date,
        comment=comment,
    )

    # create product transaction
    ProductTransaction.objects.create(
        product=product,
        quantity=-1,
        stock=product.stock,
        issuer=bank_account.account,
        transaction_id=transaction_id,
        date=date,
        comment=comment,
    )

    return transaction_id


@transaction.atomic
def change_product_price(
        product: Product,
        price: int,
        issuer: Account,
        date: datetime | None = None,
        comment: str = '',
) -> PriceChange:

    date = date or now()

    # update product price
    product.price = price

    product.save()

    # create price change object
    return PriceChange.objects.create(
        product=product,
        price=price,
        issuer=issuer,
        date=date,
        comment=comment,
    )
