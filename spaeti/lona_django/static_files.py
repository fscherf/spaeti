from lona.static_files import StyleSheet, SORT_ORDER

STATIC_FILES = [
    StyleSheet(
        name='lona-django/style.css',
        path='static/lona-django/style.css',
        url='lona-django/style.css',
        sort_order=SORT_ORDER.LIBRARY,
    ),
]
