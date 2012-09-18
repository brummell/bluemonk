from suds.client import Client
from bluemonk import app

class Issue(object):
    '''
    JIRA issue backend
    Requires suds to be installed

    Uses the following configuration values:

        ISSUES_JIRA_URL
        ISSUES_JIRA_USERNAME
        ISSUES_JIRA_PASSWORD
        ISSUES_JIRA_TYPE       The JIRA issue type
        ISSUES_JIRA_PROJECT    The JIRA project to post issues
    '''
    def __init__(self):
        url = app.config.get('ISSUES_JIRA_URL')

        self._client = Client(url)
        self._auth = client.service.login(
            app.config.get('ISSUES_JIRA_USERNAME'),
            app.config.get('ISSUES_JIRA_PASSWORD')
        )

    def submit(self, summary, description):
        issue = {
            'type': app.config.get('ISSUES_JIRA_TYPE'),
            'project': app.config.get('ISSUES_JIRA_PROJECT'),
            'summary': summary,
            'description': description
        }

        self._client.service.createIssue(self._auth, issue)
        self._client.service.logout()
