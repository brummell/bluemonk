from butterfly import Group

class GroupsProxy(object):
    def __init__(self, butterfly):
        self.group = Group(butterfly)

    def index(self, **options):
        return self.group.get_groups(**options)

    def count(self, **options):
        count = self.group.get_counts(**options)
        if not 'count' in count:
            return 0
        return int(count['count'])

    def list(self):
        groups = self.index()
        return [(g['Group']['id'], g['Group']['id']) for g in groups]

    def from_id(self, group_id, **options):
        return self.group.view_group(group_id, **options)

    def create(self, **data):
        return self.group.add_group(**data)

    def stays(self, group_id):
        return self.group.view_group_stays(group_id)

    def add_pms_group(self, group_id, pms_group):
        return self.group.add_pms_group(group_id, pms_group)

    def delete_pms_group(self, group_id, pms_group):
        return self.group.delete_pms_group(group_id, pms_group)

