"""Build a model for interacting with a psql database via SQLAlchemy."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from flask_migrate import Migrate
from . import app
from passlib.hash import sha256_crypt

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Company(db.Model):
    """Define the company model to be used in the database."""

    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.ForeignKey('portfolios.id'), nullable=False)
    symbol = db.Column(db.String(64), index=True, unique=True)
    company = db.Column(db.String(256), index=True, unique=True)
    exchange = db.Column(db.String(128))
    industry = db.Column(db.String(128))
    website = db.Column(db.String(128))
    description = db.Column(db.Text)
    CEO = db.Column(db.String(128))
    issueType = db.Column(db.String(128))
    sector = db.Column(db.String(128))

    date_created = db.Column(db.DateTime, default=dt.now())

    def __repr__(self):
        """Return dev-friendly definition."""
        return '<Company {}>'.format(self.company)


class Portfolio(db.Model):
    """Define the portfolio model to be used in the database."""

    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)

    companies = db.relationship('Company', backref='portfolio', lazy=True)

    date_created = db.Column(db.DateTime, default=dt.now())

    def __repr__(self):
        return '<Portfolio {}>'.format(self.name)


class User(db.Model):
    """Create a user for authentication."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), index=True, nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))

    portfolios = db.relationship('Portfolio', backref='user', lazy=True)

    date_created = db.Column(db.DateTime, default=dt.now())
    date_updated = db.Column(db.DateTime, default=dt.now())

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = sha256_crypt.encrypt(password)
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def check_credentials(cls, user, password):
        if user is not None:
            if sha256_crypt.verify(password, user.password):
                return True

        return False
