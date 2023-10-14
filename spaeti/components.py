from lona_picocss.html import (
    InlineButton,
    Modal,
    CLICK,
    Span,
    Icon,
    Nav,
    Div,
    Ul,
    Li,
    A,
)
from lona_html5_qrcode.html import Html5QRCodeScanner
from lona.static_files import StyleSheet, SORT_ORDER

from spaeti.lona_django import DjangoAttributeTable, DjangoTable
from spaeti.utils import format_euro_amount


class SpaetiComponent:
    STATIC_FILES = [
        StyleSheet(
            name='spaeti.css',
            path='static/spaeti.css',
            url='spaeti.css',
            sort_order=SORT_ORDER.APPLICATION,
        ),
    ]


def pformat_stock(instance):
    span = Span(str(instance.stock))

    if instance.stock < 1:
        span.style['color'] = 'red'

    return span


def pformat_quantity(instance):
    span = Span()

    if instance.quantity < 1:
        span.set_text(str(instance.quantity))
        span.style['color'] = 'red'

    elif instance.quantity > 0:
        span.set_text(f'+{str(instance.quantity)}')
        span.style['color'] = 'green'

    return span


def pformat_amount(instance):
    return format_euro_amount(
        amount_in_cent=instance.amount,
        force_sign=True,
        html=True,
    )


def pformat_balance(instance):
    return format_euro_amount(
        amount_in_cent=instance.balance,
        force_sign=False,
        html=False,
    )


def pformat_price(instance):
    return format_euro_amount(
        amount_in_cent=instance.price,
        force_sign=False,
        html=False,
    )


def pformat_account_balance(instance):
    balance = getattr(instance.get_default_bank_account(), 'balance', 0)

    return format_euro_amount(
        amount_in_cent=balance,
        force_sign=False,
        html=True,
    )


def pformat_date(instance):
    return instance.date.strftime('%c')


def pformat_created(instance):
    return instance.created.strftime('%c')


def pformat_modified(instance):
    return instance.modified.strftime('%c')


def pformat_account_flags(instance):
    return ', '.join(instance.get_flags())


def pformat_account_email(instance):
    return getattr(instance.get_user(), 'email', '')


# generic #####################################################################
class Heading(SpaetiComponent, Div):
    CLASS_LIST = ['heading']


class Actions(SpaetiComponent, Div):
    CLASS_LIST = ['actions']


class Action(SpaetiComponent, InlineButton):
    CLASS_LIST = ['action']

    def __init__(self, *args, **kwargs):
        icon = kwargs.pop('icon', '')

        super().__init__(*args, **kwargs)

        if 'handle_click' not in kwargs:
            self.events.remove(CLICK)

        if icon:
            self.nodes.insert(0, Icon(icon))


class Spacer(SpaetiComponent, Div):
    CLASS_LIST = ['spacer']


class Breadcrumb(SpaetiComponent, Div):
    CLASS_LIST = ['breadcrumb']

    def __init__(self, entries, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ul = Ul(
            Li(A('Home', href='/')),
        )

        for entry in entries:
            if isinstance(entry, (tuple, list)):
                label, url = entry

                ul.append(Li((A(label, href=url))))

            else:
                ul.append(Li(entry))

        self.nodes = [
            Nav(
                ul,
                aria_label='breadcrumb',
            ),
        ]


# QR-Codes ####################################################################
class QRCodeScanner(Div):
    def __init__(self, *args, handle_scan_result=None, **kwargs):
        super().__init__(*args, **kwargs)

        if handle_scan_result:
            self.handle_scan_result = handle_scan_result

        self.scanner = Html5QRCodeScanner(
            handle_scan_result=self._handle_scan_result,
            theme='picocss',
            autostart=False,
        )

        self.modal = Modal(closeable=False)

        self.modal.get_body().nodes = [
            self.scanner,
        ]

        self.modal.get_footer().nodes = [
            InlineButton('Cancel', handle_click=self.stop_scanning)
        ]

        self.nodes = [
            self.modal,
        ]

    def _handle_scan_result(self, scanner, data):
        self.modal.close()
        scanner.stop()

        return self.handle_scan_result(scanner, data)

    def handle_scan_result(self, scanner, data):
        return

    def start_scanning(self, input_event=None):
        self.scanner.start()
        self.modal.open()

    def stop_scanning(self, input_event=None):
        self.modal.close()
        self.scanner.stop()


# product #####################################################################
class ProductTable(SpaetiComponent, DjangoTable):
    COLUMNS = [
        ('Name', 'name'),
        ('Stock', pformat_stock),
        ('Price', pformat_price),
    ]

    RIGHT_ALIGNED_COLUMNS = [
        'Stock',
        'Price',
    ]

    def get_show_url(self, instance):
        if not self.request:
            return ''

        return self.request.server.reverse(
            'product__show',
            product_category=self.request.match_info['product_category'],
            product=instance.slug,
        )


class ProductAttributeTable(SpaetiComponent, DjangoAttributeTable):
    ROWS = [
        ('Name', 'name'),
        ('Price', pformat_price),
        ('Stock', pformat_stock),
        ('Barcode', 'barcode'),
        ('Created', pformat_created),
        ('Modified', pformat_modified),
        ('Comment', 'comment'),
    ]


class ProductTransactionTable(SpaetiComponent, DjangoTable):
    COLUMNS = [
        ('Date', pformat_date),
        ('Issuer', 'issuer'),
        ('Quantity', pformat_quantity),
        ('Comment', 'comment'),
    ]


class ProductPriceChangeTable(SpaetiComponent, DjangoTable):
    COLUMNS = [
        ('Date', pformat_date),
        ('Issuer', 'issuer'),
        ('Price', pformat_price),
        ('Comment', 'comment'),
    ]


# bank account transactions ###################################################
class BankAccountTransactionTable(SpaetiComponent, DjangoTable):
    COLUMNS = [
        ('Account', 'receiver_bank_account'),
        ('Amount', pformat_amount),
        ('Balance', pformat_balance),
        ('Date', pformat_date),
        ('Product', lambda i: i.product or ''),
        ('Comment', lambda i: i.comment or ''),
    ]


# account #####################################################################
class AccountTable(SpaetiComponent, DjangoTable):
    COLUMNS = [
        ('Username', 'username'),
        ('Email', pformat_account_email),
        ('Created', pformat_created),
        ('Flags', pformat_account_flags),
    ]

    def get_show_url(self, instance):
        if not self.request:
            return ''

        return self.request.server.reverse(
            'account__show',
            username=instance.username,
        )


class AccountAttributeTable(SpaetiComponent, DjangoAttributeTable):
    ROWS = [
        ('Username', 'username'),
        ('Email', pformat_account_email),
        ('Flags', pformat_account_flags),
        ('Balance', pformat_account_balance),
        ('Created', pformat_created),
        ('Modified', pformat_modified),
        ('Comment', 'comment'),
    ]
