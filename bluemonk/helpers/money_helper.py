from bluemonk import app
#import locale

#locale.setlocale(locale.LC_ALL, app.config.get('LOCALE', 'en_US'))
def money_to_string(price):
    if not price:
        return 'N/A'
    return "$ %s" % price
'''
    try:
        return locale.currency(float(price))
    except TypeError:
        return price
'''
app.jinja_env.filters['money_to_string'] = money_to_string
