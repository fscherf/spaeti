import pytest


@pytest.mark.django_db(transaction=True)
def test_get_spaeti_bank_account_creation():
    from spaeti import (
        SPAETI_DEFAULT_BANK_ACCOUNT_NAME,
        SPAETI_ACCOUNT_USERNAME,
    )
    from spaeti.database import get_spaeti_bank_account
    from spaeti.models import BankAccount, Account

    assert BankAccount.objects.count() == 0
    assert Account.objects.count() == 0

    # create spaeti account by calling the function the first time
    spaeti_bank_account_1 = get_spaeti_bank_account()

    # check if spaeti account was created correctly
    assert BankAccount.objects.count() == 1
    assert Account.objects.count() == 1

    assert spaeti_bank_account_1.name == SPAETI_DEFAULT_BANK_ACCOUNT_NAME
    assert spaeti_bank_account_1.account.username == SPAETI_ACCOUNT_USERNAME

    # get spaeti account a second time and check if it the same account
    spaeti_bank_account_2 = get_spaeti_bank_account()

    assert BankAccount.objects.count() == 1
    assert Account.objects.count() == 1

    assert spaeti_bank_account_1.pk == spaeti_bank_account_2.pk


@pytest.mark.django_db(transaction=True)
def test_account_creation():
    from django.contrib.auth import get_user_model

    from spaeti.database import username_is_available, add_account
    from spaeti import SPAETI_DEFAULT_BANK_ACCOUNT_NAME
    from spaeti.models import BankAccount, Account

    User = get_user_model()
    username = 'user-1'

    assert BankAccount.objects.count() == 0
    assert Account.objects.count() == 0
    assert User.objects.count() == 0

    # add account
    assert username_is_available(username)

    account = add_account(username)
    bank_account = account.get_default_bank_account()
    user = account.get_user()

    # run checks
    assert Account.objects.count() == 1
    assert BankAccount.objects.count() == 1
    assert User.objects.count() == 1

    assert account.username == username
    assert user.username == username
    assert bank_account.name == SPAETI_DEFAULT_BANK_ACCOUNT_NAME

    assert not username_is_available(username)


@pytest.mark.django_db(transaction=True)
def test_product_category_creation():
    from spaeti.database import add_product_category
    from spaeti.models import ProductCategory

    name = 'Fruit'
    name_plural = 'Fruits'

    assert ProductCategory.objects.count() == 0

    category = add_product_category(
        name=name,
        name_plural=name_plural,
    )

    # run checks
    assert category.name == name
    assert category.name_plural == name_plural
    assert category.slug == 'fruits'
    assert ProductCategory.objects.count() == 1


@pytest.mark.django_db(transaction=True)
def test_product_creation():
    from spaeti.database import add_product_category, add_product
    from spaeti.models import ProductCategory, Product

    product_category_name = 'Fruit'
    product_category_name_plural = 'Fruits'
    product_name = 'Apple'

    assert ProductCategory.objects.count() == 0
    assert Product.objects.count() == 0

    product_category = add_product_category(
        name=product_category_name,
        name_plural=product_category_name_plural,
    )

    product = add_product(
        category=product_category,
        name=product_name,
        price=1_00,
        stock=1,
    )

    # run checks
    assert ProductCategory.objects.count() == 1
    assert Product.objects.count() == 1

    assert product.category == product_category
    assert product.name == product_name
    assert product.slug == 'apple'
    assert product.price == 1_00
    assert product.stock == 1


@pytest.mark.django_db(transaction=True)
def test_product_stocking():
    from spaeti.database import (
        get_spaeti_bank_account,
        restock_product,
        add_product,
    )
    from spaeti.models import ProductTransaction

    assert ProductTransaction.objects.count() == 0

    product = add_product(
        name='product-1',
        price=1_00,
    )

    issuer = get_spaeti_bank_account().account

    transaction_id = restock_product(
        product=product,
        issuer=issuer,
        quantity=1,
    )

    # refresh database objects
    product.refresh_from_db()

    # run checks
    assert ProductTransaction.objects.count() == 1

    assert ProductTransaction.objects.get(
        transaction_id=transaction_id,
        issuer=issuer,
        product=product,
        stock=1,
    )


@pytest.mark.django_db(transaction=True)
def test_money_depositing():
    from spaeti.database import (
        get_spaeti_bank_account,
        deposit_money,
        add_account,
    )
    from spaeti.models import BankAccountTransaction

    # setup accounts
    account = add_account(username='person-1')
    spaeti_bank_account = get_spaeti_bank_account()
    bank_account = account.get_default_bank_account()

    assert BankAccountTransaction.objects.count() == 0
    assert spaeti_bank_account.balance == 0
    assert bank_account.balance == 0

    # first deposit
    transaction_id = deposit_money(
        bank_account=bank_account,
        amount=1_00,
    )

    # refresh database objects
    spaeti_bank_account.refresh_from_db()
    bank_account.refresh_from_db()

    # run checks
    assert spaeti_bank_account.balance == 1_00
    assert bank_account.balance == 1_00

    assert BankAccountTransaction.objects.get(
        transaction_id=transaction_id,
        bank_account=bank_account,
        receiver_bank_account=spaeti_bank_account,
        amount=1_00,
        balance=1_00,
    )

    assert BankAccountTransaction.objects.get(
        transaction_id=transaction_id,
        bank_account=bank_account,
        receiver_bank_account=bank_account,
        amount=1_00,
        balance=1_00,
    )

    # second deposit
    transaction_id = deposit_money(
        bank_account=bank_account,
        amount=20_00,
    )

    # refresh database objects
    spaeti_bank_account.refresh_from_db()
    bank_account.refresh_from_db()

    # run checks
    assert spaeti_bank_account.balance == 21_00
    assert bank_account.balance == 21_00

    assert BankAccountTransaction.objects.get(
        transaction_id=transaction_id,
        bank_account=bank_account,
        receiver_bank_account=spaeti_bank_account,
        amount=20_00,
        balance=21_00,
    )

    assert BankAccountTransaction.objects.get(
        transaction_id=transaction_id,
        bank_account=bank_account,
        receiver_bank_account=bank_account,
        amount=20_00,
        balance=21_00,
    )


@pytest.mark.django_db(transaction=True)
def test_product_buying():
    from spaeti.database import (
        restock_product,
        buy_product,
        add_product,
        add_account,
    )
    from spaeti.models import BankAccountTransaction, ProductTransaction

    # setup database
    product = add_product(
        name='product-1',
        price=1_00,
        stock=0,
    )

    bank_account = add_account(
        username='person-1',
    ).get_default_bank_account()

    assert BankAccountTransaction.objects.count() == 0
    assert ProductTransaction.objects.count() == 0

    # try to buy a product that is out of stock
    with pytest.raises(RuntimeError):
        buy_product(
            bank_account=bank_account,
            product=product,
        )

    restock_product(
        product=product,
        quantity=10,
    )

    # first buy
    transaction_id = buy_product(
        bank_account=bank_account,
        product=product,
    )

    # refresh database objects
    product.refresh_from_db()
    bank_account.refresh_from_db()

    # run checks
    assert product.stock == 9
    assert bank_account.balance == -1_00

    assert BankAccountTransaction.objects.get(
        transaction_id=transaction_id,
        bank_account=bank_account,
        product=product,
        amount=-1_00,
        balance=-1_00,
    )

    assert ProductTransaction.objects.get(
        transaction_id=transaction_id,
        product=product,
        quantity=-1,
        stock=9,
    )


@pytest.mark.django_db(transaction=True)
def test_change_product_price():
    from spaeti.database import change_product_price, add_product, add_account

    # setup database
    account = add_account(username='person-1')

    product = add_product(
        name='product-1',
        price=1_00,
        stock=0,
    )

    # change price
    change_product_price(
        product=product,
        issuer=account,
        price=2_00,
        comment='Price increase',
    )

    # refresh database objects
    product.refresh_from_db()

    # run checks
    price_changes = product.price_changes.order_by('date')

    assert product.price == 2_00

    assert price_changes[0].price == 1_00
    assert price_changes[0].comment == 'Initial price'

    assert price_changes[1].price == 2_00
    assert price_changes[1].comment == 'Price increase'
