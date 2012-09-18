from flask.ext.wtf import Form, TextField, SubmitField, HiddenField, Required, URL, Length
from flask.ext.wtf.html5 import URLField

class HotelForm(Form):
    id = TextField("Id", validators=[Length(min=36, max=36)])
    name = TextField("Name", validators=[Length(max=40)])
    butterfly_url = URLField("Butterfly URL", validators=[URL()])
    butterfly_user = TextField("Butterfly user", validators=[Length(max=10)])
    butterfly_token = TextField("Butterfly token", validators=[Length(40)])
    shorthand = TextField("Shorthand", validators=[Length(max=5)])
    cups_address = TextField("Cups IP address", validators=[Length(max=200)])
    cups_password = TextField("Cups password", validators=[Length(max=200)])

class HotelDeleteForm(Form):
    id = HiddenField(validators=[Required()])
    delete = SubmitField("Delete")

