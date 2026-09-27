from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from .fields import DatalistField

class Invoices(FlaskForm):
        customer = DatalistField("Customer")
        invoice_num = StringField("Invoice Number")
        min_total = FloatField("Minimum Total", validators=[NumberRange(min=0.0)])
        max_total = FloatField("Maximum Total", validators=[NumberRange(min=0.0)])
        submit = SubmitField("Submit")

class NewInvoice(Invoices):
        customer = DatalistField("Customer", validators=[DataRequired()])
        invoice_num = StringField("Invoice Number", validators=[DataRequired()])
        min_total = FloatField("Minimum Total", validators=[NumberRange(min=0.0), DataRequired()])
        max_total = FloatField("Maximum Total", validators=[NumberRange(min=0.0), DataRequired()])
