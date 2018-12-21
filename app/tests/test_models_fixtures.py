"""Tests to ensure conftest fixtures match expected models."""
from ..models import Company


def test_company_all(session):
    """Test that company database is empty."""
    companies = Company.query.all()
    assert len(companies) == 0


def test_company_name(company):
    """Test that Company test object is names correctly."""
    assert company.company == 'Microsoft'


def test_create_company(company):
    """Test that company has an id."""
    assert company.id > 0


def test_create_portfolio(portfolio):
    """Test that portfolio has an id."""
    assert portfolio.id > 0


def test_portfolio_id(portfolio):
    """Test that portfolio user has an id."""
    assert portfolio.user_id > 0


def test_user_create(user):
    """Test user has an id."""
    assert user.id > 0


def test_user_email(user):
    """Test user email data."""
    assert user.email == 'user@user.com'
