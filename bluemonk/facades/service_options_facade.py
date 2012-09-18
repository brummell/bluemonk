from flask import g

from bluemonk.libs.facade import Facade
from bluemonk.forms.service_option import ServiceOptionForm
from bluemonk.components.paginator import Paginator
from bluemonk import app

def index(page):
    limit = app.config.get('PAGINATOR_PER_PAGE', 25)
    serviceOptions = g.proxies.ServiceOptions.index(page=page, limit=limit)
    count = g.proxies.ServiceOptions.count()

    serviceGroups = dict(g.proxies.ServiceGroups.list())

    paginator = Paginator(page, limit, count)
    facade = Facade(serviceOptions=serviceOptions, serviceGroups=serviceGroups, paginator=paginator)
    return facade

def add():
    form = ServiceOptionForm()
    facade = Facade(form=form)

    serviceGroups = g.proxies.ServiceGroups.index()

    groups = g.proxies.ServiceGroups.list()
    form.service_group_id.choices = groups

    if form.validate_on_submit():
        serviceOption = g.proxies.ServiceOptions.create(**form.data)
        facade['service_option_id'] = serviceOption['ServiceOption']['id']
        facade.successful = True

    return facade

def view(service_option_id):
    serviceOption = g.proxies.ServiceOptions.from_id(service_option_id)
    if not serviceOption:
        abort(404)

    serviceGroup = g.proxies.ServiceGroups.from_id(serviceOption['ServiceOption']['service_group_id'])

    facade = Facade(serviceOption=serviceOption, serviceGroup=serviceGroup)
    return facade

def edit(service_option_id):
    serviceOption = g.proxies.ServiceOptions.from_id(service_option_id)
    if not serviceOption:
        abort(404)

    form = ServiceOptionForm(**serviceOption['ServiceOption'])
    facade = Facade(form = form, serviceOption=serviceOption)

    groups = g.proxies.ServiceGroups.list()
    form.service_group_id.choices = groups

    if form.validate_on_submit():
        serviceOption = g.proxies.ServiceOptions.update(service_option_id, **form.data)
        facade['service_option_id'] = service_option_id
        facade.successful = True
    return facade
