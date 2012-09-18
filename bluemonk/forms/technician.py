from flask.ext.wtf import Form, TextField, SubmitField, HiddenField, Required,\
        Length, BooleanField, PasswordField

class TechnicianForm(Form):
    name = TextField("Name", validators=[Required(), Length(max=40)])
    login = TextField("Login", validators=[Required(), Length(max=10)])
    active = BooleanField('Active', default=True)

class TechnicianAddForm(TechnicianForm):
    password = PasswordField("Password", validators=[Required()])
