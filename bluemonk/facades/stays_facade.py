from flask import g, flash

from bluemonk import app
from bluemonk.libs.facade import Facade
from bluemonk.components.paginator import Paginator

from bluemonk.forms.room_search import RoomSearchForm
from bluemonk.forms.navigator import NavigatorControlsForm
from bluemonk.forms.printqueue_controls import PrintQueueControlsForm
from bluemonk.forms.stay import StayAddPurchaseForm
import json

def index(page):
    limit = app.config.get('PAGINATOR_PER_PAGE', 25)
    stays = g.proxies.Stays.index(active=True, page=page, with_rooms=True, with_guests=True, limit=limit)
    count = g.proxies.Stays.count(active=True)
    paginator = Paginator(page, limit, count)

    return Facade(stays=stays, paginator=paginator)

def view(stay_id):
    stay = g.proxies.Stays.from_id(
        stay_id, with_guest=True, with_room=True, with_passport_account=True
    )

    if not stay:
        return None

    printerConfigurationId = stay['Room'].get('printer_configuration_id', None)
    if printerConfigurationId:
        printerConfiguration = g.proxies.PrinterConfigurations.from_id(printerConfigurationId)
        stay['PrinterConfiguration'] = printerConfiguration
    else:
        stay['PrinterConfiguration'] = None

    navigator = g.proxies.Navigators.from_id(stay['Room']['navigator_id'])

    group = g.proxies.Groups.from_id(stay['Stay']['group_id']) if stay['Stay']['group_id'] else None

    navigator_id = navigator['Navigator']['id'] if navigator else None

    navigatorControlsForm = NavigatorControlsForm(id=navigator_id)
    return Facade(
        navigator=navigator, group=group, navigator_id=navigator_id,
        navigatorControlsForm =navigatorControlsForm, stay=stay
    )

def search():
    form = RoomSearchForm()
    count = g.proxies.Stays.count(active=True)
    facade = Facade(form=form, stays_count = count)
    return facade

def print_queue(stay_id):

    printQueue = g.proxies.Stays.printjobs(stay_id)
    if not printQueue:
        abort(404)

    guest_id = printQueue['Stay']['guest_id']
    printQueue['Guest'] = g.proxies.Guests.from_id(guest_id)

    printers = g.proxies.Printers.index()
    printer_choices = [(p.id, p.name) for p in printers]

    forms = {}
    for printjob in printQueue['StayPrintjob']:
        item_id = printjob['id']
        form = PrintQueueControlsForm(id = item_id, hotel_id = hotel_id, stay_id = stay_id)
        form.printer_id.choices = printer_choices
        forms[item_id] = form

    return Facade(stay=printQueue, forms=forms)

def print_queue_actions(stay_id, item_id):
    form = PrintQueueControlsForm()
    if form.validate_on_submit():
        result = g.proxies.StayPrintjobs.print_item(form.data)

def by_room_number():
    form = RoomSearchForm()
    room_number = form.room_number.data
    facade = Facade(form=form, room_number=room_number)

    if form.validate_on_submit():
        options = dict(
            room_number=room_number, active=form.active.data,
            with_guests=True
        )
        stays = g.proxies.Stays.index(**options)

        if not stays:
            facade.empty_results = True
            flash('No stays were found for room %s' % room_number, 'error')
            return facade

        for stay in stays:
            stay['Room'] = {'room_number' : form.room_number.data}

        facade['stays'] = stays
        facade.successful = True

    return facade

def purchases(stay_id):
    stay = g.proxies.Stays.from_id(
        stay_id, with_room=True, with_passport_account=True
    )
    if not stay:
        abort(404)
    purchases = g.proxies.Stays.purchases(stay_id)
    serviceGroups = dict(g.proxies.ServiceGroups.list())

    return Facade(stay=stay, purchases=purchases, serviceGroups=serviceGroups)

def add_purchase(stay_id):
    stay = g.proxies.Stays.from_id(stay_id, with_room=True)
    if not stay:
        abort(404)

    form = StayAddPurchaseForm(stay_id=stay_id)
    form.service_option_id.choices = g.proxies.ServiceOptions.list()
    facade = Facade(form=form, stay=stay)
    if form.validate_on_submit():
        g.proxies.Stays.add_purchase(stay_id, form.data)
        facade.successful = True
    return facade

def update(stay_id, form_options):
    things = {}
    for k in form_options.keys():
        try:
            things[k] = json.loads(form_options.get(k))
            
        except(ValueError):
            things[k] = form_options.get(k)
            
    return g.proxies.Stays.update(stay_id, **things)
