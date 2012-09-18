from bluemonk import app

# This fixes the warning pycountry prints out in the console if no logger is
# set for pycountry.db
import logging
logging.getLogger('pycountry.db').addHandler(logging.NullHandler())

from pycountry import languages

def iso_to_name(iso):
    if not iso:
        return 'Unknown'
    try:
        language = languages.get(alpha2=iso)
    except KeyError as e:
        return 'Unknown'
    return language.name

app.jinja_env.filters['language_iso_to_name'] = iso_to_name
