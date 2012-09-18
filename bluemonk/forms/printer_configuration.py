from flask.ext.wtf import Form, TextAreaField, TextField, Required

class PrinterConfigurationForm(Form):
    name = TextField("Name", validators=[Required()])
    configuration = TextField("Configuration Name", validators=[Required()])
    description = TextAreaField("Description", validators=[Required()])

