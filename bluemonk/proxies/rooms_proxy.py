from butterfly import Room

class RoomsProxy(object):
    def __init__(self, butterfly):
        self.room = Room(butterfly)

    def index(self, **options):
        return self.room.get_rooms(**options)

    def count(self, **options):
        count = self.room.get_room_count(**options)
        if not 'count' in count:
            return 0
        return int(count['count'])

    def from_id(self, room_id, **options):
        return self.room.view_room(room_id, **options)

    def create(self, **data):
        return self.room.add_room(**data)

    def update(self, room_id, **data):
        return self.room.update_room(room_id, **data)

