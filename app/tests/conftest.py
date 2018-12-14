from ..models import db as _db
from .. import app as _app
import pytest
import os
from ..models import Company, Portfolio


@pytest.fixture()
def app(request):
    _app.config.from_mapping(
        TESTING=True,
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.getenv('TEST_DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=False,
    )
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture()
def db(app, request):

    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture()
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture()
def company(session):
    company = Company(
        symbol='goog',
        company='Alphabet, Inc.',
        portfolio_id=1,
        )

    session.add(company)
    session.commit()
    return company


@pytest.fixture()
def portfolio(session):
    portfolio = Portfolio(name='name')

    session.add(portfolio)
    session.commit()
    return portfolio
