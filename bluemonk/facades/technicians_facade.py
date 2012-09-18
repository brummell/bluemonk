from flask import g, flash
from bluemonk.libs.facade import Facade

from bluemonk.forms.technician import TechnicianForm, TechnicianAddForm

def add():
    form = TechnicianAddForm()
    facade = Facade(form=form)
    if form.validate_on_submit():
        flash('Technician account created.', 'success')
        result = g.proxies.Technicians.create(**form.data)
        facade.successful = True

    return facade

def edit(technician_id):
    technician = g.proxies.Technicians.from_id(technician_id)
    if not technician:
        abort(404)

    form = TechnicianForm(**technician['Technician'])
    facade = Facade(form=form, technician=technician)
    if form.validate_on_submit():
        flash('Technician account updated.', 'success')
        result = g.proxies.Technicians.update(technician_id, **form.data)
        facade.successful = True
    return facade
