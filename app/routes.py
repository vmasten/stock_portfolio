"""Define the routes used by the stock portfolio app."""
from . import app
from flask import Flask, render_template, abort, redirect, url_for
from sqlalchemy.exc import IntegrityError
from .models import Company, db
from json import JSONDecodeError
import requests as req
import json
from .forms import StockSearchForm


@app.route('/')
def home():
    """Render base route, a homepage."""
    return render_template('home.html'), 200


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Go to the search page, which has a form for an API call."""
    form = StockSearchForm()

    if form.validate_on_submit():
        res = req.get(f'https://api.iextrading.com/1.0/stock/{ form.data["stock_name"] }/company')

        try:
            data = json.loads(res.text)
            company = {
                'symbol': data['symbol'],
                'companyName': data['companyName'],
                'exchange': data['exchange'],
                'industry': data['industry'],
                'website': data['website'],
                'description': data['description'],
                'CEO': data['CEO'],
                'issueType': data['issueType'],
                'sector': data['sector'],
            }

            new_company = Company(**company)
            try:
                db.session.add(new_company)
                db.session.commit()
            except IntegrityError:
                return redirect(url_for('.portfolio')), 201
                # there's probably a more graceful way

            return redirect(url_for('.portfolio')), 302

        except JSONDecodeError:
            abort(404)

    return render_template('search.html', form=form), 200


@app.route('/portfolio')
def portfolio():
    """Render the portfolio page."""
    return render_template('stock_detail.html', db=db), 200
