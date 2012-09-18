from bluemonk import app

def display_openid(openid):
    if not openid:
        return ''
    rv = openid
    if rv.startswith(('http://', 'https://')):
        rv = rv.split('/', 2)[-1]
    return rv.rstrip('/')
app.jinja_env.filters['display_openid'] = display_openid
