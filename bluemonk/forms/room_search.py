from flask.ext.wtf import Form, TextField, BooleanField, Required

class RoomSearchForm(Form):
    room_number = TextField('Room Number', validators=[Required()])
    active = BooleanField('Active Stays', default=True)
