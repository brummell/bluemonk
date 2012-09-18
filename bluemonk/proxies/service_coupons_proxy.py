from butterfly import ServiceCoupon

class ServiceCouponsProxy(object):

    def __init__(self, butterfly):
        self.service_coupon = ServiceCoupon(butterfly)

    def index(self, **options):
        return self.service_coupon.get_service_coupons(**options)

    def from_id(self, service_coupon_id, **options):
        return self.service_coupon.view_service_coupon(service_coupon_id, **options)

    def create(self, **data):
        return self.service_coupon.add_service_coupon(**data)

    def update(self, service_coupon_id, **data):
        return self.service_coupon.update_coupon(service_coupon_id, **data)

    def count(self):
        response = self.service_coupon.get_service_coupons_count()
        if not 'count' in response:
            return 0

        return int(response['count'])
