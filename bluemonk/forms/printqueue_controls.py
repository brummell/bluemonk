from flask.ext.wtf import Form, SubmitField, HiddenField, SelectField, Required

class PrintQueueControlsForm(Form):

    id = HiddenField(validators=[Required()])
    stay_id = HiddenField(validators=[Required()])
    hotel_id = HiddenField(validators=[Required()])
    printer_id = SelectField(validators=[Required()])
    print_item = SubmitField("Print")
