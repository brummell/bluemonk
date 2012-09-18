from butterfly import StayPrintjob

class StayPrintjobsProxy(object):
    def __init__(self, butterfly):
        self.stay_printjob = StayPrintjob(butterfly)

    def index(self, **options):
        return self.stay_printjob.get_printjobs(**options)

    def count(self, **options):
        count = self.stay_printjob.get_printjob_count(**options)
        if not 'count' in count:
            return 0
        return int(count['count'])

    def from_id(self, printjob_id, **options):
        return self.stay_printjob.view_printjob(printjob_id, **options)

    def print_item(self, data):
        printer_id = data['printer_id']
        printjob_id = data['id']
        stay_id = data['stay_id']

        printjob = self.from_id(printjob_id)
        if not printjob['StayPrintjob']['stay_id'] == stay_id:
            return False

        return self.stay_printjob.print_printjob(printjob_id = printjob_id, printer_id = printer_id)
