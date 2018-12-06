from flask import Flask, render_template, abort, redirect, url_for, session, g, make_response
from sqlalchemy.exc import IntegrityError

from json import JSONDecodeError
import requests as req
import json
import os
from .forms import StockSearchForm

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# def fetch_stocks(stock):
#     return req.get(f"{os.getenv('API_URL')}/stock/{stock}/company")

@app.route('/')
def home():
    """Render base route, a homepage."""
    return render_template('home.html'), 200


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Go to the search page, which has a form for an API call."""
    form = StockSearchForm()

    if form.validate_on_submit():
        stock = form.data['stock_name']
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

            # new_company = Company(**company)
            # db.session.add(new_company)
            # db.session.commit()
            return redirect((url_for('.stock_detail.html')))

        except JSONDecodeError:
            abort(404)

    return render_template('search.html', form=form), 200

