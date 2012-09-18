from flask.ext.wtf import Form, SubmitField, TextField, TextAreaField, HiddenField, Required, Length

class GroupForm(Form):
    id = TextField("Group name", validators=[Required(), Length(min=1, max=16)])
    description = TextAreaField("Description")

class GroupPmsForm(Form):
    pms_group = TextField("PMS Group", validators=[Required()])

class GroupPmsRemoveForm(Form):
    pms_group = HiddenField("PmsGroup", validators=[Required()])
    delete = SubmitField("Dissociate", validators=[Required()])
