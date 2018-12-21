"""Global fixtures for use in testing."""

from ..models import db as _db
from .. import app as _app
import pytest
import os
from ..models import Company, Portfolio, User


@pytest.fixture()
def app(request):
    """Global instance of app for testing."""
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
    """Global database for testing."""
    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture()
def session(db, request):
    """Session for use in testing."""
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
def client(app, db, session):
    """Client for testing."""
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture()
def flask_session(client):
    """Create session for testing."""
    with client.session_transaction() as flask_session:
        yield flask_session


@pytest.fixture()
def user(session):
    """User object for testing."""
    user = User(
        email='user@user.com',
        password='password',
        first_name='John',
        last_name='Smith')

    session.add(user)
    session.commit()
    return user


@pytest.fixture()
def authenticated_client(client, user):
    """Test of user authentication process."""
    client.post(
        '/login',
        data={'email': user.email, 'password': 'password'},
        follow_redirects=True,
    )
    yield client

    client.get('/logout')


@pytest.fixture()
def portfolio(session, user):
    """Portfolio object for testing."""
    portfolio = Portfolio(name='test', user_id=user.id)

    session.add(portfolio)
    session.commit()
    return portfolio


@pytest.fixture()
def company(session, portfolio):
    """Company object for testing."""
    company = Company(company='Microsoft', symbol='msft', portfolio_id=portfolio.id)

    session.add(company)
    session.commit()
    return company
