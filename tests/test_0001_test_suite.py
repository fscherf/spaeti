import pytest


@pytest.mark.parametrize('browser_name', ['chromium', 'firefox', 'webkit'])
async def test_browser_tests(browser_name, spaeti):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await getattr(p, browser_name).launch()
        browser_context = await browser.new_context()
        page = await browser_context.new_page()

        await page.goto(spaeti.make_url('/'))
        await page.wait_for_selector('#lona h1:has-text("Späti")')


@pytest.mark.django_db(transaction=True)
def test_database_setup():
    from django.db import transaction

    from spaeti.models import (
        ProductTransaction,
        AccountTransaction,
        ProductCategory,
        Product,
        Account,
        Person,
    )

    with transaction.atomic():
        assert ProductTransaction.objects.count() == 0
        assert AccountTransaction.objects.count() == 0
        assert ProductCategory.objects.count() == 0
        assert Account.objects.count() == 0
        assert Product.objects.count() == 0
        assert Person.objects.count() == 0
