"""Define the routes used by the stock portfolio app."""
from . import app
from flask import Flask, render_template, abort, redirect, url_for, flash, session
from sqlalchemy.exc import IntegrityError, DBAPIError
from .models import Company, db
from json import JSONDecodeError
import requests as req
import json
from .forms import StockSearchForm, StockAddForm


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


@app.route('/portfolio')
def portfolio():
    """Render the portfolio page."""
    db = Company.query.all()
    return render_template('stock_detail.html', db=db)
