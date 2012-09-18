from butterfly import ServicePurchase

class ServicePurchasesProxy(object):
    def __init__(self, butterfly):
        self.service_purchase = ServicePurchase(butterfly)

    def index(self, **options):
        return self.service_purchase.get_purchases(**options)

    def count(self, **options):
        response = self.service_purchase.get_purchase_count(**options)
        if not 'count' in response:
            return 0

        return int(response['count'])

    def from_id(self, service_purchase_id, **options):
        return self.service_purchase.view_purchase(service_purchase_id, **options)

    def create(self, **data):
        return self.service_purchase.add_purchase(**data)
