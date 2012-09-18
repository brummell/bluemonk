from __future__ import absolute_import
from bluemonk import app
from celery import Celery
celery = Celery('bluemonk', broker=app.config.get('CELERY_BROKER_URL'))
