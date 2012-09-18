from flask.ext.wtf import Form, TextField, Required,\
        Length, BooleanField, SelectField

class RoomForm(Form):

    room_number = TextField('Room Number', validators=[Required()])
    floor = TextField('Floor', validators=[Required()])
    printer_configuration_id = SelectField("Printer Configuration")
    room_class_id = SelectField("Room Class")
    voip_user = TextField('VOIP User')
    voip_password = TextField('VOIP Password')
