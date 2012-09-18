from flask import g
from bluemonk import app
from bluemonk.components.paginator import Paginator
from bluemonk.libs.facade import Facade
from bluemonk.forms.navigator import NavigatorAddForm, NavigatorEditForm, NavigatorRoomForm, NavigatorControlsForm

def index(page):
    '''
    Paginates all the navigators
    '''

    limit = app.config.get('PAGINATOR_PER_PAGE', 25)
    count = g.proxies.Navigators.count()
    navigators = g.proxies.Navigators.index(page=page, limit=limit)
    paginator = Paginator(page, limit, count)
    facade = Facade(navigators=navigators, paginator=paginator)
    return facade

def add():
    form = NavigatorAddForm()
    facade = Facade(form=form)
    if form.validate_on_submit():
        navigator = g.proxies.Navigators.create(**form.data)
        facade['navigator_id'] = navigator['Navigator']['id']
        facade.successful = True
    return facade

def view(navigator_id):
    '''
    View a specific navigator
    '''

    navigator = g.proxies.Navigators.from_id(navigator_id, with_room=True)
    if not navigator:
        abort(404)
    form = NavigatorRoomForm(navigator_id = navigator['Navigator']['id'])
    return Facade(navigator=navigator, room_move_form = form)

def edit(navigator_id):
    navigator = g.proxies.Navigators.from_id(navigator_id)
    if not navigator:
        abort(404)
    form = NavigatorEditForm(**navigator['Navigator'])
    facade = Facade(form=form, navigator=navigator)

    if form.validate_on_submit():
        updated = g.proxies.Navigators.update(navigator_id, **form.data)
        facade.successful = True
    return facade

def controls(navigator_id):
    form = NavigatorControlsForm()

    facade = Facade(form=form)

    if form.validate_on_submit():
        results = g.proxies.Navigators.handle_controls(form.data)
        if not results is False:
            facade.successful = True
            facade['results'] = results
    return facade

def room_move(navigator_id):
    form = NavigatorRoomForm(navigator_id = navigator_id)
    facade = Facade(form=form)

    if form.validate_on_submit():
        rooms = g.proxies.Rooms.index(room_number=form.room_number.data)
        if len(rooms) == 0:
            flash("The specified room does not exists.", 'error')
            return facade
        room = g.proxies.Rooms.update(rooms[0]['Room']['id'], navigator_id=form.navigator_id.data)
        print room
        facade.successful = True

    return facade
