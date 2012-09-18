from butterfly import ServiceGroup

class ServiceGroupsProxy(object):
    def __init__(self, butterfly):
        self.service = ServiceGroup(butterfly)

    def index(self, **options):
        return self.service.get_service_groups(**options)

    def list(self, **options):
        serviceGroups = self.index(**options)
        return [(sg['ServiceGroup']['id'], sg['ServiceGroup']['name']) for sg in serviceGroups]

    def count(self, **options):
        response = self.service.service_group_count(**options)
        if not 'count' in response:
            return 0

        return int(response['count'])

    def from_id(self, service_group_id, **options):
        return self.service.view_service_group(service_group_id, **options)

    def create(self, **data):
        return self.service.add_service_group(**data)

    def update(self, service_group_id, **data):
        return self.service.update_service_group(service_group_id, **data)
