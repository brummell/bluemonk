from flask import g

from bluemonk import app
from bluemonk.libs.facade import Facade
from bluemonk.components.paginator import Paginator

def index(page):
    limit = app.config.get('PAGINATOR_PER_PAGE', 25)
    servicePurchases = g.proxies.ServicePurchases.index(page=page, limit=limit,
            with_service_options=True
    )

    serviceGroups = dict(g.proxies.ServiceGroups.list())

    count = g.proxies.ServicePurchases.count()

    paginator = Paginator(page, limit, count)

    facade = Facade(servicePurchases=servicePurchases, paginator=paginator, serviceGroups=serviceGroups)
    return facade

def view(service_purchase_id):
    servicePurchase = g.proxies.ServicePurchases.from_id(
        service_purchase_id, with_stay=True
    )
    if not servicePurchase:
        abort(404)

    facade = Facade(servicePurchase=servicePurchase)
    return facade
