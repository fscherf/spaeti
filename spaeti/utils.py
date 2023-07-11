import os


def env_get_bool(name, default=''):
    env_var = os.environ.get(name, default).strip().lower()

    return env_var in ('1', 'true', 'yes')


def env_get_int(name, default='0'):
    return int(os.environ.get(name, default))


def debug_is_enabled():
    return env_get_bool('SPAETI_DEBUG')


def test_suite_is_running():
    return env_get_bool('SPAETI_TESTING')


def format_euro_amount(amount_in_cent, html=False):
    euro = amount_in_cent // 100
    cent = int(((amount_in_cent / 100) - (amount_in_cent // 100)) * 100)

    prefix = ''
    color = 'black'

    if amount_in_cent > 0:
        prefix = '+'
        color = 'green'

    elif amount_in_cent < 0:
        prefix = '-'
        color = 'red'

    # FIXME
    amount_string = f"{prefix}{'{:,}'.format(euro, ',').replace(',', '.')},{cent:02d}€"  # NOQA

    if html:
        return f'<span style="color: {color}">{amount_string}</span>'

    return amount_string
