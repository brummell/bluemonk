from flask import render_template
from flask.ext.mail import Message

class UserVerificationMessage(Message):
    def __init__(self, **kwargs):
        Message.__init__(self, "Bluemonk Account Verification")

        required = ['to', 'user_id', 'verification_token']
        for k in required:
            if not k in kwargs:
                msg = "These values must be provided: %s" % ",".join(required)
                raise KeyError(msg)

        self.add_recipient(kwargs['to'])
        self.body = render_template('emails/user_verification.txt', **kwargs)
        self.html = render_template('emails/user_verification.html', **kwargs)
