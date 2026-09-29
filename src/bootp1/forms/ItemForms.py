from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from .fields import DatalistField

class Items(FlaskForm):
        name = DatalistField("Item Name")
        description = StringField("Description")
        min_rate = FloatField("Minimum Rate", validators=[NumberRange(min=0.0)])
        max_rate = FloatField("Maximum Rate", validators=[NumberRange(min=0.0)])
        submit = SubmitField("Submit")

class NewItem(FlaskForm):
        name = StringField("Item Name", validators=[DataRequired()])
        default_description = StringField("Description", validators=[DataRequired()])
        default_rate = FloatField("Rate", validators=[DataRequired(), NumberRange(min=0.0)])
        submit = SubmitField("Submit")

