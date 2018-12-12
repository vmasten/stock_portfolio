"""Define a form to be used by Flask for user input."""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class StockSearchForm(FlaskForm):
    """A simple class that helps build a form to get a stock name."""

    symbol = StringField('symbol', validators=[DataRequired()])

class StockAddForm(FlaskForm):
    symbol = StringField('symbol', validators=[DataRequired()])
    company = StringField('company', validators=[DataRequired()])
