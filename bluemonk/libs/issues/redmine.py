from pyactiveresource.activeresource import ActiveResource

from bluemonk import app
from bluemonk.libs.issues import Issue

class Issue(ActiveResource):
    '''
    Redmine issue backend

    Uses the following app configuration values:
        ISSUES_REDMINE_URL
        ISSUES_REDMINE_USER
        ISSUES_REDMINE_PASSWORD
        ISSUES_REDMINE_PROJECT    The project issues will be posted to
        ISSUES_REDMINE_TRACKER    The tracker used for issues
    '''
    def __init__(self):
        self._site = app.config.get('ISSUES_REDMINE_URL')
        self._user = app.config.get('ISSUES_REDMINE_USER')
        self._password = app.config.get('ISSUES_REDMINE_PASSWORD')

        self.project = app.config.get('ISSUES_REDMINE_PROJECT')

        ActiveResource.__init__(self)

    def submit(self, summary, description):
        issue = {
            'project_id': app.config.get('ISSUES_REDMINE_PROJECT'),
            'tracker': app.config.get('ISSUES_REDMINE_TRACKER'),
            'subject': summary,
            'description': description
        }
