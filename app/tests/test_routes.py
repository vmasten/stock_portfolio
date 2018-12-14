"""Tests for routing in the stock_portfolio app."""
import pytest
from sqlalchemy.exc import IntegrityError


def test_home_route_get(app):
    """Test for the home route."""
    rv = app.test_client().get('/')
    assert rv.status_code == 200
    assert b'<h1>Stock Portfolio Builder</h1>' in rv.data


def test_home_route_post(app):
    """Test a post on home route."""
    rv = app.test_client().post('/')
    assert rv.status_code == 405


def test_home_route_delete(app):
    """Test deletion on home route."""
    rv = app.test_client().delete('/')
    assert rv.status_code == 405


def test_portfolio_route_get(app, session):
    """Test the portfolio route."""
    rv = app.test_client().get('/portfolio')
    assert rv.status_code == 200
    assert b'<h2>Stock Portfolio</h2>' in rv.data



def test_search_route_get(app, session):
    """Test the search route."""
    rv = app.test_client().get('/search')
    assert rv.status_code == 200
    assert b'<a href="/portfolio">here</a>' in rv.data


def test_search_post_pre_redirect(app, session):
    rv = app.test_client().post('/search', data={'symbol': 'aapl'})
    assert rv.status_code == 302


def test_search_post(app, session):
    rv = app.test_client().post('/search', data={'symbol': 'amzn'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'<input type="submit" value="Add">' in rv.data


def test_no_symbol(app, session):
    rv = app.test_client().post('search', data={'symbol': ''})
    assert rv.status_code == 200


def test_404_exception(app):
    rv = app.test_client().get('/blackhole')
    assert rv.status_code == 404


# def test_company_route(app, session, db, portfolio, company):
#     rv = app.test_client().get('/company')
#     assert rv.status_code == 200
#     assert b'Company' in rv.data
