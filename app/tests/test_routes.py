"""Tests for routing in the stock_portfolio app."""
from ..models import Portfolio


def test_authenticated_client(authenticated_client):
    """Test authenticated client fixture."""
    assert authenticated_client


def test_portfolio_fixture(portfolio, user):
    """Test portfolio fixture."""
    assert Portfolio.query.first().id == portfolio.id
    assert portfolio.user_id == user.id
    assert not Portfolio.query.first().companies


def test_home_route_get(client):
    """Test for the home route."""
    res = client.get('/')
    assert res.status_code == 200
    assert b'<h1>Stock Portfolio Builder</h1>' in res.data


def test_home_route_delete(app):
    """Test deletion on home route."""
    rv = app.test_client().delete('/')
    assert rv.status_code == 405


def test_registration_route(client):
    """Test registration route for unauthenticated user."""
    res = client.get('register')
    assert res.status_code == 200


def test_registration_redirect(client):
    """Test registering new user."""
    res = client.post(
        '/register',
        data={
            'email': 'user@user.com',
            'password': 'pass',
            'first_name': 'jerk',
            'last_name': 'mode'},
        follow_redirects=True,
    )
    assert b'Login' in res.data


def test_login(client):
    """Test login functionality."""
    client.post(
        '/register',
        data={
            'email': 'user@user.com',
            'password': 'pass',
            'first_name': 'jerk',
            'last_name': 'mode'},
        follow_redirects=True,
    )
    res = client.post(
        '/login',
        data={
            'email': 'user@user.com',
            'password': 'pass'},
        follow_redirects=True
    )
    assert res.status_code == 200


def test_authenticated_user(authenticated_client):
    """See if an authenticated user can access gated content."""
    res = authenticated_client.get('/search')
    assert res.status_code == 200


def test_company_to_portfolio_creation(authenticated_client, portfolio):
    """Test adding a company to a portfolio with created status code."""
    authenticated_client.post('/search', data={'symbol': 'tsla'}, follow_redirects=True)
    form_data = {'symbol': 'tsla', 'company': 'Tesla', 'portfolios': portfolio.id}
    rv = authenticated_client.post(
        '/company',
        data=form_data,
        follow_redirects=False)
    assert len(Portfolio.query.first().companies) == 1
    assert rv.status_code == 302


def test_company_to_portfolio_redirect(authenticated_client, portfolio):
    """Test adding a company to the portfolio with redirect."""
    authenticated_client.post('/search', data={'symbol': 'tsla'}, follow_redirects=True)
    form_data = {'symbol': 'tsla', 'company': 'Tesla', 'portfolios': portfolio.id}
    rv = authenticated_client.post(
        '/company',
        data=form_data,
        follow_redirects=True)
    assert rv.status_code == 200
    assert b'<h3>Make a Portfolio</h3>' in rv.data


def test_logout(authenticated_client):
    """Test logout functionality."""
    res = authenticated_client.get('/logout', follow_redirects=True)
    assert res.status_code == 200


def test_not_logged_in_user(client):
    """Test authentication gating."""
    rv = client.get('/portfolio')
    assert rv.status_code == 404
