from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired

from bootp1.forms.fields import DatalistField

class Customers(FlaskForm):
        name = DatalistField("Customer Name")
        contact_first_name = StringField("Contact First Name")
        contact_last_name = StringField("Contact Last Name")
        contact_phone = StringField("Contact Phone Number")
        submit = SubmitField("Submit")

class NewCustomer(Customers):
        name = StringField("Customer Name", validators=[DataRequired()])
