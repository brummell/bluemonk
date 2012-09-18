from butterfly import Guest

class GuestsProxy(object):
    def __init__(self, butterfly):
        self.guest = Guest(butterfly)

    def index(self, **options):
        return self.guest.get_guest(**options)

    def count(self, **options):
        return self.guest.get_counts(**options)

    def from_id(self, guest_id, **options):
        return self.guest.view_guest(guest_id, **options)
