from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from .fields import DatalistField
from .ItemForms import Item

class Invoices(FlaskForm):
        customer = DatalistField("Customer")
        invoice_num = StringField("Invoice Number")
        min_total = FloatField("Minimum Total", validators=[NumberRange(min=0.0)])
        max_total = FloatField("Maximum Total", validators=[NumberRange(min=0.0)])
        submit = SubmitField("Submit")

class NewInvoice(FlaskForm):
        customer = DatalistField("Customer", validators=[DataRequired()])
        invoice_num = StringField("Invoice Number", validators=[DataRequired()])
        items = FieldList(FormField(Item), min_entries=1, max_entries=10)
        total = FloatField("Total", validators=[DataRequired(), NumberRange(min=0.0)])
        submit = SubmitField("Submit")
