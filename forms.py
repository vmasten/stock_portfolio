from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class StockSearchForm(FlaskForm):
    """A simple class that helps build a form to get a stock name."""
    stock_name = StringField('symbol', validators=[DataRequired()])
