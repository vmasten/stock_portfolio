from . import app
from .models import db
import pytest
import os

@pytest.fixture
def client():
    def do_nothing():
        pass

    db.session.commit = do_nothing
    yield app.test_client()
    db.session.rollback()

    app.config.from_mapping(
        TESTING=True,
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.getenv('TEST_DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=False
    )
