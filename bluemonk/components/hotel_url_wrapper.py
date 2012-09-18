from functools import wraps
from flask import g, request, redirect, url_for, render_template as o_render_template

from butterfly import Butterfly

from bluemonk.proxies import Proxies
from bluemonk.models.hotel import Hotel

def load_hotel(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'hotel_id' in kwargs:
            return f(*args, **kwargs)

        g.hotel_id = kwargs['hotel_id']

        g.hotel = Hotel.query.filter_by(id=g.hotel_id).first()
        if not g.hotel:
            return o_render_template('hotel_not_found.html'), 404

        if not g.hotel.validate_butterfly():
            return redirect(url_for('hotel_misconfigured', hotel_id=g.hotel_id))

        g.butterfly = Butterfly(
            g.hotel.butterfly_user, g.hotel.butterfly_token,
            g.hotel.butterfly_url
        )
        g.proxies = Proxies(g.butterfly)

        return f(*args, **kwargs)
    return decorated_function

def render_template(template, **kwargs):
    if not 'hotel_id' in kwargs and g.hotel_id:
        kwargs['hotel_id'] = g.hotel_id
    if not 'hotel' in kwargs and g.hotel:
        kwargs['hotel'] = g.hotel
    return o_render_template(template, **kwargs)
