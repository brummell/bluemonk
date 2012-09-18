from butterfly import RoomClass

class RoomClassesProxy(object):
    def __init__(self, butterfly):
        self.room_class = RoomClass(butterfly)

    def index(self, **options):
        return self.room_class.get_room_classes(**options)

    def from_id(self, room_class_id, **kwargs):
        return self.room_class.view_room_class(room_class_id, **kwargs)

    def create(self, **kwargs):
        return self.room_class.add_room_class(**kwargs)

    def update(self, room_class_id, **kwargs):
        return self.room_class.update_room_class(room_class_id, **kwargs)

    def list(self):
        roomClasses = self.index()
        return [(rc['RoomClass']['id'], rc['RoomClass']['name']) for rc in roomClasses]
