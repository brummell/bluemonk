from flask import g, abort

from bluemonk.libs.facade import Facade
from bluemonk.forms.printer_configuration import PrinterConfigurationForm

def add():
    form = PrinterConfigurationForm()
    facade = Facade(form=form)
    if form.validate_on_submit():
        printerConfiguration = g.proxies.PrinterConfigurations.create(**form.data)
        facade['printer_configuration_id'] = printerConfiguration['PrinterConfiguration']['id']
        facade.successful=True
    return facade

def edit(printer_configuration_id):
    printerConfiguration = g.proxies.PrinterConfigurations.view(printer_configuration_id)

    if not printerConfiguration:
        abort(404)

    form = PrinterConfigurationForm(**printerConfiguration['PrinterConfiguration'])
    facade = Facade(form=form, printerConfiguration=printerConfiguration)
    if form.validate_on_submit():
        printerConfiguration = g.proxies.PrinterConfigurations.update(printer_configuration_id, **form.data)
        facade.successful = True
    return facade

