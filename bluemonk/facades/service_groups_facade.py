from flask import g

from bluemonk.libs.facade import Facade
from bluemonk.forms.service_group import ServiceGroupForm
from bluemonk.components.paginator import Paginator
from bluemonk import app

def index(page):
    limit = app.config.get('PAGINATOR_PER_PAGE', 25)
    serviceGroups = g.proxies.ServiceGroups.index(page=page,limit=limit)
    count = g.proxies.ServiceGroups.count()

    paginator = Paginator(page, limit, count)
    facade = Facade(serviceGroups=serviceGroups, paginator=paginator)
    return facade

def add():
    form = ServiceGroupForm()
    facade = Facade(form=form)
    if form.validate_on_submit():
        result = g.proxies.ServiceGroups.create(**data)
        facade.successful = True
    return facade

def edit(service_group_id):
    serviceGroup = g.proxies.ServiceGroups.from_id(service_group_id)
    if not serviceGroup:
        abort(404)

    form = ServiceGroupForm(**serviceGroup['ServiceGroup'])
    facade = Facade(form=form, serviceGroup=serviceGroup)
    if form.validate_on_submit():
        result = g.proxies.ServiceGroups.update(service_group_id, **form.data)
        facade.successful = True

    return facade

def view(service_group_id):
    serviceGroup = g.proxies.ServiceGroups.from_id(service_group_id, with_service_options=True, with_service_coupons=True)
    facade = Facade(serviceGroup=serviceGroup)
    return facade
