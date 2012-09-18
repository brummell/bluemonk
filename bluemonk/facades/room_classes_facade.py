from flask import g
from bluemonk.libs.facade import Facade
from bluemonk.forms.room_class import RoomClassForm

def index(page):
    roomClasses = g.proxies.RoomClasses.index()
    printerConfigurations = dict(g.proxies.PrinterConfigurations.list())
    return Facade(roomClasses=roomClasses, printerConfigurations=printerConfigurations)

def view(room_class_id):
    roomClass = g.proxies.RoomClasses.from_id(room_class_id)
    if not roomClass:
        abort(404)

    printerConfigurations = dict(g.proxies.PrinterConfigurations.list())
    facade = Facade(roomClass=roomClass, printerConfigurations=printerConfigurations)
    return facade

def create():
    form = RoomClassForm()

    printerConfigurations = g.proxies.PrinterConfigurations.list()
    printerConfigurations.insert(0, ("none", "Default"))
    form.printer_configuration_id.choices = printerConfigurations

    facade = Facade(form=form)
    if form.validate_on_submit():
        if form.printer_configuration_id.data == 'none':
            form.printer_configuration_id.data = ''

        roomClass = g.proxies.RoomClasses.create(**form.data)
        facade.successful = True
    return facade

def update(room_class_id):

    roomClass = g.proxies.RoomClasses.from_id(room_class_id)
    if not roomClass:
        abort(404)

    form = RoomClassForm(**roomClass['RoomClass'])
    facade = Facade(form=form, roomClass=roomClass)

    printerConfigurations = g.proxies.PrinterConfigurations.list()
    printerConfigurations.insert(0, ("none", "Default"))

    form.printer_configuration_id.choices = printerConfigurations

    if form.validate_on_submit():
        if form.printer_configuration_id.data == 'none':
            form.printer_configuration_id.data = ''
        print form.data
        roomClass = g.proxies.RoomClasses.update(room_class_id, **form.data)
        facade.successful = True
    return facade
