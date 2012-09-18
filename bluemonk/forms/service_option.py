from flask.ext.wtf import Form, TextField, SubmitField, HiddenField, Required,\
        Length, BooleanField, PasswordField, DateTimeField, SelectField

from flask.ext.wtf.html5 import IntegerField

#TODO Custom price validator, see service coupons
class ServiceOptionForm(Form):
    name = TextField("Name", validators=[Required()])
    price = TextField("Price", validators=[Required()])
    credit_only = BooleanField("Credit Only")
    coupon_only = BooleanField("Coupon Only")
    service_group_id = SelectField("Service Group", validators=[Required()])

