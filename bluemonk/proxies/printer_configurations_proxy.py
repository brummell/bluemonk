from butterfly import PrinterConfiguration

class PrinterConfigurationsProxy(object):
    def __init__(self, butterfly):
        self.printer_configuration = PrinterConfiguration(butterfly)

    def index(self, **options):
        return self.printer_configuration.get_printer_configurations(**options)

    def from_id(self, printer_configuration_id, **options):
        return self.printer_configuration.get_printer_configuration(printer_configuration_id, **options)

    def create(self, **data):
        return self.printer_configuration.add_printer_configuration(**data)

    def update(self, printer_configuration_id, **data):
        return self.printer_configuration.update_printer_configuration(printer_configuration_id, **data)

    def view(self, printer_configuration_id):
        return self.printer_configuration.get_printer_configuration(printer_configuration_id)

    def list(self):
        printerConfigurations = self.index()
        return [(pc['PrinterConfiguration']['id'], pc['PrinterConfiguration']['name']) for pc in printerConfigurations]

