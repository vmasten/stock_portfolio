from ..models import db, Company
import pytest


def test_company_all(session):
    companies = Company.query.all()
    assert len(companies) == 0
