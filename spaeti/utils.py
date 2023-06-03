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
