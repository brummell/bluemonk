from flask import g
from bluemonk import app
from bluemonk.libs.facade import Facade
from bluemonk.components.paginator import Paginator

def index(page):
    limit = app.config.get('PAGINATOR_PER_PAGE', 25)
    printJobs = g.proxies.StayPrintjobs.index(page=page,limit=limit)
    count = g.proxies.StayPrintjobs.count()

    paginator = Paginator(page, limit, count)
    facade = Facade(stayPrintJobs=printJobs, paginator=paginator)
    return facade

def view(stay_printjob_id):
    printJob = g.proxies.StayPrintjobs.from_id(stay_printjob_id)
    if not printJob:
        abort(404)
    return Facade(stayPrintJob=printJob)

def print_out(printer_id, stay_printjob_id):
    pass
