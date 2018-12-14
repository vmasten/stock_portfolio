"""Define a form to be used by Flask for user input."""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired
from .models import Portfolio


class StockSearchForm(FlaskForm):
    """A simple class that helps build a form to get a stock name."""

    symbol = StringField('symbol', validators=[DataRequired()])


class StockAddForm(FlaskForm):
    """A form to add stock information to the database."""
    symbol = StringField('symbol', validators=[DataRequired()])
    company = StringField('company', validators=[DataRequired()])
    exchange = StringField('exchange', validators=[DataRequired()])
    industry = StringField('industry', validators=[DataRequired()])
    website = StringField('website', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    CEO = StringField('CEO', validators=[DataRequired()])
    issueType = StringField('issueType', validators=[DataRequired()])
    sector = StringField('sector', validators=[DataRequired()])

    portfolios = SelectField('portfolios')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.portfolios.choices = [(str(p.id), p.name) for p in Portfolio.query.all()]


class PortfolioCreateForm(FlaskForm):
    """Create a form to add a Portfolio to the database."""
    name = StringField('name', validators=[DataRequired()])


class AuthForm(FlaskForm):
    """Form to create an account."""
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
