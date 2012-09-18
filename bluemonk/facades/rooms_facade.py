from flask import g, abort

from bluemonk import app
from bluemonk.libs.facade import Facade
from bluemonk.components.paginator import Paginator
from bluemonk.forms.room import RoomForm
def index(page):
    limit = app.config.get('PAGINATOR_PER_PAGE', 25)
    count = g.proxies.Rooms.count()

    rooms = g.proxies.Rooms.index(page=page, limit=limit)
    paginator = Paginator(page, limit, count)
    facade = Facade(rooms=rooms, paginator=paginator)
    return facade

def view(room_id):
    room = g.proxies.Rooms.from_id(room_id)
    if not room:
        abort(404)

    printerConfiguration = None
    roomClass = None

    if room['Room']['room_class_id']:
        roomClass = g.proxies.RoomClasses.from_id(room['Room']['room_class_id'])

    if room['Room']['printer_configuration_id']:
        printerConfiguration = g.proxies.PrinterConfiguration.from_id(room['Room']['printer_configuration_id'])

    facade = Facade(room=room, printerConfiguration=printerConfiguration,roomClass=roomClass)
    return facade

def add():
    printerConfigurations = g.proxies.PrinterConfigurations.list()
    roomClasses = g.proxies.RoomClasses.list()

    printerConfigurations.insert(0, ("none", "Default"))
    roomClasses.insert(0, ("none", "Default"))

    form = RoomForm()
    facade = Facade(form=form)

    form.printer_configuration_id.choices = printerConfigurations
    form.room_class_id.choices = roomClasses

    if form.validate_on_submit():
        if form.printer_configuration_id.data == 'none':
            form.printer_configuration_id.data = ''
        if form.room_class_id.data == 'none':
            form.room_class_id.data = ''
        room = g.proxies.Rooms.create(**form.data)
        print form.data
        print room
        facade['room_id'] = room['Room']['id']
        facade.successful = True
    return facade

def edit(room_id):
    room = g.proxies.Rooms.from_id(room_id)
    if not room:
        aborT(404)

    printerConfigurations = g.proxies.PrinterConfigurations.list()
    roomClasses = g.proxies.RoomClasses.list()

    printerConfigurations.insert(0, ("none", "Default"))
    roomClasses.insert(0, ("none", "Default"))

    form = RoomForm(**room['Room'])
    facade = Facade(form=form, room=room)

    form.printer_configuration_id.choices = printerConfigurations
    form.room_class_id.choices = roomClasses
    if form.validate_on_submit():
        if form.printer_configuration_id.data == 'none':
            form.printer_configuration_id.data = ''
        if form.room_class_id.data == 'none':
            form.room_class_id.data = ''
        room = g.proxies.Rooms.update(room_id, **form.data)
        print room
        facade['room_id'] = room['Room']['id']
        facade.successful = True
    return facade
