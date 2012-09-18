from flask import g
from bluemonk import app
from bluemonk.components.paginator import Paginator
from bluemonk.libs.facade import Facade
from bluemonk.forms.group import GroupForm, GroupPmsForm, GroupPmsRemoveForm

def add():
    form = GroupForm()
    facade = Facade(form=form)
    if form.validate_on_submit():
        group = g.proxies.Groups.create(**form.data)
        facade['group_id'] = group['Group']['id']
        facade.successful = True
    return facade

def edit(group_id):
    form = GroupForm()
    facade = Facade(form=form)
    if form.validate_on_submit():
        group = g.proxies.Groups.update_group(group_id, **form.data)
        facade['group_id'] = group['Group']['group_id']
        facade.successful = True
    return facade

def view(group_id, page):
    limit = app.config.get('PAGINATOR_PER_PAGE', 25)
    group = g.proxies.Groups.from_id(group_id, with_pms_groups=True)
    if not group:
        abort(404)

    stays = g.proxies.Stays.index(page=page, active=True, group_id=group_id, with_rooms=True)
    stays_count = g.proxies.Stays.count(active=True, group_id=group_id)

    paginator = Paginator(page, limit, stays_count)
    forms = {}
    for pmsGroup in group['PmsGroup']:
        forms[pmsGroup['id']] = GroupPmsRemoveForm(pms_group=pmsGroup['pms_group'])

    return Facade(deleteForms = forms, group=group, stays=stays, stays_count=stays_count, paginator=paginator)

def link_pms_group(group_id):
    group = g.proxies.Groups.from_id(group_id)
    if not group:
        abort(404)

    form = GroupPmsForm()
    facade = Facade(form=form, group=group)
    if form.validate_on_submit():
        print g.proxies.Groups.add_pms_group(group_id, form.pms_group.data)
        facade.successful = True
    return facade

def unlink_pms_group(group_id):
    form = GroupPmsRemoveForm()
    facade = Facade(form=form)
    if form.validate_on_submit():
        print g.proxies.Groups.delete_pms_group(group_id, form.pms_group.data)
        facade.successful = True
    return facade

def delete(group_id):
    g.proxies.Groups.delete(group_id)
