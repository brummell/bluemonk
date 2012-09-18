from flask import g, abort

from bluemonk import app
from bluemonk.libs.facade import Facade
from bluemonk.components.paginator import Paginator
from bluemonk.forms.service_coupon import ServiceCouponForm
from dateutil.parser import parse as date_parser

def index(page):
    limit = app.config.get('PAGINATOR_PER_PAGE', 25)
    count = g.proxies.ServiceCoupons.count()

    serviceCoupons = g.proxies.ServiceCoupons.index(with_service_group=True, page=page, limit=limit)


    paginator = Paginator(page, limit, count)
    facade = Facade(serviceCoupons=serviceCoupons, paginator=paginator)
    return facade

def view(service_coupon_id):
    serviceCoupon = g.proxies.ServiceCoupons.from_id(service_coupon_id, with_service_group=True)

    if not serviceCoupon:
        abort(404)

    return Facade(serviceCoupon=serviceCoupon)

def add():
    form = ServiceCouponForm()

    facade = Facade(form=form)

    groups = g.proxies.ServiceGroups.list()
    form.service_group_id.choices = groups

    if form.validate_on_submit():
        serviceCoupon = g.proxies.ServiceCoupons.create(**form.data)
        facade['service_coupon_id'] = serviceCoupon['ServiceCoupon']['id']
        facade.successful = True
    return facade


def edit(service_coupon_id):
    serviceCoupon = g.proxies.ServiceCoupons.from_id(service_coupon_id)
    if not serviceCoupon:
        abort(404)

    serviceCoupon['ServiceCoupon']['starts'] = date_parser(serviceCoupon['ServiceCoupon']['starts'])
    serviceCoupon['ServiceCoupon']['expires'] = date_parser(serviceCoupon['ServiceCoupon']['expires'])
    form = ServiceCouponForm(**serviceCoupon['ServiceCoupon'])
    facade = Facade(form = form, serviceCoupon=serviceCoupon)

    groups = g.proxies.ServiceGroups.list()
    form.service_group_id.choices = groups

    if form.validate_on_submit():
        serviceCoupon = g.proxies.ServiceCoupons.update(service_coupon_id, **form.data)
        facade['service_coupon_id'] = serviceCoupon['ServiceCoupon']['id']
        facade.successful = True
    return facade
