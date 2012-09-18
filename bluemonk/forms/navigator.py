from flask.ext.wtf import Form, TextField, Required, BooleanField, HiddenField, SubmitField

class NavigatorEditForm(Form):
    billing_enabled = BooleanField('Billing Enabled')
    authorized_boot = BooleanField('Boot Authorized')

class NavigatorAddForm(NavigatorEditForm):
    id = TextField('Asset Tag', validators=[Required()])

class NavigatorRoomForm(Form):
    navigator_id = HiddenField("Navigator", validators=[Required()])
    room_number = TextField('Room Number', validators=[Required()])

class NavigatorControlsForm(Form):
    id = HiddenField(validators=[Required()])
    reboot = SubmitField("Reboot")
    authorize = SubmitField("Authorize")
    reboot_authorize = SubmitField("Reboot and Authorize")
    ping = SubmitField("Ping")
