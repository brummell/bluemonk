from flask.ext.wtf import Form, TextField, SelectField, BooleanField, Required, \
        TextAreaField

class MailForm(Form):

    sender = SelectField("Sender", validators=[Required()])
    subject = TextField("Subject", validators=[Required()])
    content = TextAreaField("Message", validators=[Required()])
    important = BooleanField("Important")

    recipients = SelectField('Recipients', validators=[Required()])
    groups = SelectField("Groups")
    rooms = TextField("Rooms")
    floors = TextField("Floors")
