from bluemonk import app, celery

@celery.task
def submit(Issue, summary, description):
    Issue().submit(summary, description)
