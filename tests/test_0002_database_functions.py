import pytest


@pytest.mark.django_db(transaction=True)
def test_deposit():
    from spaeti.database import get_spaeti_account, deposit_money, add_account

    spaeti_account = get_spaeti_account()
    account = add_account(username='user1', email='user1@example.org')
