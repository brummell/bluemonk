from flask.ext.wtf import Form, TextField, SubmitField, HiddenField, Required,\
        Length, BooleanField, PasswordField, DateTimeField, SelectField

from flask.ext.wtf.html5 import IntegerField
from datetime import datetime

#TODO might want to use https://github.com/trentrichardson/jQuery-Timepicker-Addon

class ServiceCouponForm(Form):
    code = TextField("Coupon Code", validators=[Required(), Length(max=10)])
    description = TextField("Description", validators=[Required()])
    discount = TextField("Discount", validators=[Required()]) #TODO Custom validator for discount
    per_guest_max_uses = IntegerField("Per Guest Max Uses")
    total_max_uses = IntegerField("Total Max Uses")
    active = BooleanField("Active")
    starts = DateTimeField("Starts On", validators=[Required()], default=datetime.now())
    expires = DateTimeField("Expires On", validators=[Required()], default=datetime.now())
    service_group_id = SelectField("Service Group", validators=[Required()])
