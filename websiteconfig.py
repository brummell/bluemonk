import os

_basedir = os.path.abspath(os.path.dirname(__file__))

#Server name must be set for Celery tasks to generate proper urls.
#SERVER_NAME='10.0.0.20:5000'

DATABASE_URI = 'sqlite:///%s' % os.path.join(_basedir, 'bluemonk.sqlite')
DATABASE_CONNECT_OPTIONS = {}

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 1

DEFAULT_MAIL_SENDER = 'Bluemonk'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_FAIL_SILENTLY = False

USE_CELERY=True
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# CSRF
SECRET_KEY = 'herpaderp'

# ISSUES
ISSUES_ENABLED = True
ISSUES_BACKEND = 'bluemonk.libs.issues.jira'

from issues_jira import *
#from issue_redmine import *

del os
