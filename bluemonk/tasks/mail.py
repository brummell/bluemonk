from bluemonk import app, celery
from flask.ext.mail import Mail

@celery.task
def send(MessageClass, **kwargs):
    # The Flask-Mail extension requires the app context to exist to instantiate
    # the message.
    with app.test_request_context() as request:
        mailer = Mail(app)
        mailer.send(MessageClass(**kwargs))

