from flask.ext.wtf import Form, TextField, SubmitField, HiddenField, Required,\
        Length, BooleanField, PasswordField

class ServiceGroupForm(Form):
    name = TextField("Name", validators=[Required(), Length(max=40)])
    description = TextField("Description", validators=[Required(), Length(max=10)])
    active = BooleanField('Active', default=True)
