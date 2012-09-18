from butterfly import ServiceOption

class ServiceOptionsProxy(object):
    def __init__(self, butterfly):
        self.service_option = ServiceOption(butterfly)

    def index(self, **options):
        return self.service_option.get_service_options(**options)

    def count(self, **options):
        response = self.service_option.get_service_option_count(**options)
        if not 'count' in response:
            return 0

        return int(response['count'])

    def list(self, **options):
        serviceOptions = self.index(**options)
        return [(so['ServiceOption']['id'], so['ServiceOption']['name']) for so in serviceOptions]

    def from_id(self, service_option_id):
        return self.service_option.view_service_option(service_option_id)

    def create(self, **data):
        return self.service_option.add_service_option(**data)

    def update(self, service_option_id, **data):
        return self.service_option.update_service_option(service_option_id, **data)
