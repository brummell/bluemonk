import cups
from flask import g, abort


class CupsError(RuntimeError):
    '''
    Wraps the connection errors from cups into a management exception.
    '''
    pass

class PrintersProxy(object):
    def __init__(self, butterfly):
        cups.setPasswordCB(self.password_response)
        cups.setUser("cups_ctrl")
        self.bad_password = False
        self.IPP_STATUS_CODES = {cups.IPP_PRINTER_IDLE : "IDLE", cups.IPP_PRINTER_PROCESSING : "PROCESSING", cups.IPP_PRINTER_STOPPED: "STOPPED"}

    def password_response(self, x):
        if self.bad_password:
            print "BAD PASSWORD"
            raise RuntimeError

        self.bad_password = True
        return g.hotel.cups_password

    def get_connection(self):
        try:
            connection = cups.Connection(host=g.hotel.cups_address)
        except RuntimeError as e:
            raise CupsError(e)
        return connection


    def index(self):
        try:
            conn = self.get_connection()
            printers = conn.getPrinters()
            self.bad_password = False
            for printer in printers:
                printers[printer]['printer-state-label'] = self.IPP_STATUS_CODES[printers[printer]['printer-state']]
            return printers
        except (cups.IPPError) as e:
            abort(403)

    def enable_printer(self, printer_id):
        try:
            conn = self.get_connection()
            conn.enablePrinter(printer_id)
            self.bad_password = False
        except (cups.IPPError) as e:
            abort(403)

    def disable_printer(self, printer_id):
        try:
            conn = self.get_connection()
            conn.disablePrinter(printer_id)
            self.bad_password = False
        except (cups.IPPError) as e:
            abort(403)

    def get_jobs(self):
        try:
            conn = self.get_connection()
            jobs = conn.getJobs(requested_attributes=["job-id", 'printer-uri', 'time-at-creation', 'time-at-processing', 'time-at-completed', 'job-state', 'job-state-reasons'])
            self.bad_password = False
            return jobs
        except (cups.IPPError) as e:
            abort(403)


    def cancel_job(self, job_id):
        try:
            conn = self.get_connection()
            conn.cancelJob(int(job_id))
            self.bad_password = False
        except (cups.IPPError) as e:
            abort(403)

    def cancel_all_jobs(self, printer_id):
        jobs = self.get_jobs()
        try:
            conn = self.get_connection()
            for job_id in jobs:
                job = jobs[job_id]
                if jobs[job_id]['printer-uri'].endswith(printer_id):
                    conn.cancelJob(int(job_id))
            self.bad_password = False
        except (cups.IPPError) as e:
            abort(403)

