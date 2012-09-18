from flask.ext.wtf import Form, TextField, Required,\
        Length, BooleanField, SelectField

class RoomClassForm(Form):

    name = TextField("Name", validators=[Required()])
    is_always_authorized = BooleanField("Can Always Boot")

    printer_configuration_id = SelectField("Printer Configuration")

    billing_enabled = BooleanField("Billing Enabled", default=True)
    screensaver_enabled = BooleanField("Idle Screen Enabled", default=True)
