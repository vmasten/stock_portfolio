"""Define the routes used by the stock portfolio app."""
from . import app
from flask import Flask, render_template, redirect, url_for, flash, session
from sqlalchemy.exc import IntegrityError, DBAPIError
from .models import Company, db, Portfolio
import requests as req
import json
from .forms import StockSearchForm, StockAddForm, PortfolioCreateForm


@app.add_template_global
def get_portfolios():
    """Check whether portfolio database entries currently exist."""
    return Portfolio.query.all()


@app.route('/')
def home():
    """Render base route, a homepage."""
    return render_template('home.html'), 200


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Go to the search page, which has a form for an API call."""
    form = StockSearchForm()

    if form.validate_on_submit():
        res = req.get(f'https://api.iextrading.com/1.0/stock/{form.data["symbol"]}/company')

        data = json.loads(res.text)
        session['context'] = data

        return redirect(url_for('.company'))

    return render_template('search.html', form=form), 200


@app.route('/company', methods=['GET', 'POST'])
def company():
    form_context = {
        'symbol': session['context']['symbol'],
        'company': session['context']['companyName'],
        'exchange': session['context']['exchange'],
        'industry': session['context']['industry'],
        'website': session['context']['website'],
        'description': session['context']['description'],
        'CEO': session['context']['CEO'],
        'issueType': session['context']['issueType'],
        'sector': session['context']['sector'],
    }

    form = StockAddForm(**form_context)
    if form.validate_on_submit():
        try:
            company = Company(
                symbol=form.data['symbol'],
                company=form.data['company'],
                exchange=form.data['exchange'],
                industry=form.data['industry'],
                website=form.data['website'],
                description=form.data['description'],
                CEO=form.data['CEO'],
                issueType=form.data['issueType'],
                sector=form.data['sector'],
                portfolio_id=form.data['portfolios']
            )
            db.session.add(company)
            db.session.commit()
        except (DBAPIError, IntegrityError):
            flash('Something went wrong with your search.')
            return render_template('search.html', form=form)

        return redirect(url_for('.portfolio'))

    return render_template(
        'company.html',
        form=form,
        company=form.data['company'],
        symbol=form.data['symbol'],
    )


@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    """Render the portfolio page."""

    form = PortfolioCreateForm()

    if form.validate_on_submit():
        try:
            portfolio = Portfolio(name=form.data['name'])
            db.session.add(portfolio)
            db.session.commit()
        except (DBAPIError, IntegrityError):
            flash('Something went wrong on the form.')
            return render_template('stock_detail.html', form=form)

        return redirect(url_for('.search'))

    companies = Company.query.all()
    portfolios = Portfolio.query.all()
    return render_template('stock_detail.html', companies=companies, portfolios=portfolios, form=form)
