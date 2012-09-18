from bluemonk import app

def guest_name(guest):
    if not guest:
        return ''
    return "%s %s" % (guest['first_name'], guest['last_name'])

app.jinja_env.filters['guest_name'] = guest_name
