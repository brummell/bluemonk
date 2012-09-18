from flask.ext.wtf import Form, BooleanField, HiddenField, SelectField, Required, Length, DateTimeField


class StayAddPurchaseForm(Form):
    stay_id = HiddenField("Stay", validators=[Required()])
    service_option_id = SelectField('Service Option', validators=[Required()])
    is_credited = BooleanField('Credited (free)')
