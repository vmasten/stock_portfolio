"""Module to allow logins on the site."""
from flask import render_template, flash, redirect, url_for, session, abort, g
from .models import db, User
from .forms import AuthForm, RegisterForm
from . import app
import functools


def login_required(view):
    """Ensure the user can only see the login page initially."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            abort(404)

        return view(**kwargs)

    return wrapped_view


@app.before_request
def load_logged_in_user():
    """Get the user being logged in."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Allow the user to register a new login."""
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        first_name = form.data['first_name']
        last_name = form.data['last_name']
        error = None

        if not email or not password:
            error = 'Invalid email or password'
        if User.query.filter_by(email=email).first() is not None:
            error = f'{email} has already been registered.'

        if error is None:
            user = User(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name)

            db.session.add(user)
            db.session.commit()

            flash('Registration complete. You may now log in.')
            return redirect(url_for('.login'))

        flash(error)

    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate user."""
    form = AuthForm()
    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        error = None

        user = User.query.filter_by(email=email).first()

        if user is None or not User.check_credentials(user, password):
            error = 'Invalid username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('.portfolio'))

        flash(error)

    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    """Log the user out."""
    session.clear()
    flash('Thanks for visiting!')
    return redirect(url_for('.login'))
