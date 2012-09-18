from butterfly import Technician

class TechniciansProxy(object):
    def __init__(self, butterfly):
        self.technician = Technician(butterfly)

    def index(self, **options):
        return self.technician.get_technicians(**options)

    def from_id(self, technician_id):
        return self.technician.view_technician(technician_id)

    def create(self, **data):
        return self.technician.add_technician(**data)

    def update(self, technician_id, **data):
        return self.technician.update_technician(technician_id, **data)
