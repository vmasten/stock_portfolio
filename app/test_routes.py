"""Tests for routing in the stock_portfolio app."""
from . import app
from .models import db
import pytest



@pytest.fixture
def client():
    def do_nothing():
        pass

    db.session.commit = do_nothing
    yield app.test_client()
    db.session.rollback()

def test_home_route_get():
    """Test for the home route."""
    rv = app.test_client().get('/')
    assert rv.status_code == 200
    assert b'<h1>Welcome to your future!</h1>' in rv.data


def test_home_route_post():
    """Test a post on home route."""
    rv = app.test_client().post('/')
    assert rv.status_code == 405


def test_home_route_delete():
    """Test deletion on home route."""
    rv = app.test_client().delete('/')
    assert rv.status_code == 405


def test_portfolio_route_get():
    """Test the portfolio route."""
    rv = app.test_client().get('/portfolio')
    assert rv.status_code == 200
    assert b'<h2>Company Info</h2>' in rv.data


def test_search_route_get():
    """Test the search route."""
    rv = app.test_client().get('/search')
    assert rv.status_code == 200
    assert b'<h1>Search for stocks</h1>' in rv.data


def test_search_post_pre_redirect(client):
    rv = client.post('/search', data = {'symbol' : 'aapl'})
    assert rv.status_code == 200


def test_search_post(client):
    rv = client.post('/search', data = {'symbol' : 'aapl'})
    assert rv.status_code == 200
    assert b'<h2>Company Info</h2>' in rv.data

def test_bunk_symbol(client):
    rv = client.post('search', data={'symbol' : ''})
    assert rv.status_code == 404
