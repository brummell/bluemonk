from bluemonk import app
from bluemonk.tasks.issues import submit
from time import strftime
import importlib

class Issue(object):
    '''
    Generates an issue on a ticket tracker.

    The following app configuration values are used:
        USE_CELERY        Asynchronous(True) or Synchronous(False)
        ISSUES_ENABLED     Enables the issue generator
        ISSUES_BACKEND     Use this class as issue backend. (jira, redmine, etc.)

    See each specific backend for their configuration values.
    '''
    def __init__(self, user_id, email):

        self.original_user_id = user_id
        self.original_email = email
        self.created_on = strftime("%Y-%m-%d %H:%M:%S")

        backend = importlib.import_module(app.config.get('ISSUES_BACKEND'))
        print backend
        if not backend:
            raise RuntimeError("Issue class not found: `%s`" % issue)

        self.issue = backend.Issue

    def submit(self, summary, description):
        '''
        Submit the issue using the choosen backend.
        Will either do it in a blocking or non-blocking (asynchronous) way
        depending on the USE_CELERY configuration flag.
        '''
        if not app.get('ISSUES_ENABLED', False):
            return True

        description = "Posted on %s from Bluemonk by %s\n\n%s" % (
            self.created_on,
            self.original_email,
            self.original_user_id,
        )

        if app.config.get('USE_CELERY', False):
            task = submit.delay(self.issue, summary, description)
            return task

        return self.issue().submit(summary, description)
