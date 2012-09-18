from flask import g
from bluemonk.libs.facade import Facade
from bluemonk.forms.navigator import NavigatorControlsForm

def view(passport_account_id):
    passportAccount = g.proxies.PassportAccount.from_id(passport_account_id)
    if not passportAccount:
        abort(404)
    facade = Facade(passportAccount=passportAccount)
    return facade
