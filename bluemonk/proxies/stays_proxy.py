from butterfly import Stay

class StaysProxy(object):
    def __init__(self, butterfly):
        self.stay = Stay(butterfly)

    def index(self, **options):
        return self.stay.get_stays(**options)

    def count(self, **options):
        response = self.stay.get_stay_count(**options)
        if not 'count' in response:
            return 0
        return int(response['count'])

    def from_id(self, stay_id, **options):
        return self.stay.view_stay(stay_id, **options)

    def purchases(self, stay_id, **options):
        return self.stay.get_purchases(stay_id, **options)

    def printjobs(self, stay_id, **options):
        return self.stay.get_printjobs(stay_id, **options)

    def add_purchase(self, stay_id, data):

        if data['is_credited']:
            payment_method = 'credit'
        else:
            payment_method = 'pms'

        purchases = {
            'items': [
                {'service_option_id': data['service_option_id']}
            ],
            'payment_method': payment_method
        }
        return self.stay.add_purchase(stay_id, purchases)

    def update(self, stay_id, **options):
        return self.stay.update_stay(stay_id, **options)
