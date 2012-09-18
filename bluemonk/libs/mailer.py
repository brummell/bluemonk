from bluemonk import app
from flask.ext.mail import Mail, email_dispatched
from bluemonk.tasks.mail import send

class Mailer(Mail):
    def send(self, MessageClass, **kwargs):
        if app.config.get('USE_CELERY', False):
            task = send.delay(MessageClass, **kwargs)
            return True

        return Mail.send(self, MessageClass(**kwargs))
