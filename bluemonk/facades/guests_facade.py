from flask import g
from bluemonk.libs.facade import Facade

def view(guest_id):
    guest = g.proxies.Guests.from_id(guest_id)
    if not guest:
        abort(404)
    return Facade(guest=guest)
