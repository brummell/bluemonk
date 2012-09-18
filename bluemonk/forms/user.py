from flask.ext.wtf import Form, TextField, SubmitField, HiddenField, Required,\
        Length, SelectField, BooleanField

from bluemonk.models.user import roles

class UserForm(Form):
    name = TextField("Name", validators=[Length(max=40)])
    role = SelectField("Role", coerce=int, validators=[Required()], choices=roles.items())
    active = BooleanField('Active', default=True)

class UserSendVerificationForm(Form):
    id = HiddenField(validators=[Required()])
    send = SubmitField("Send Verification")

class UserDeleteForm(Form):
    user_id = TextField(validators=[Required()])
