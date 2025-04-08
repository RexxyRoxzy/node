import os
import requests
import json
import stripe
from flask import Flask, render_template, redirect, url_for, flash, request, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.middleware.proxy_fix import ProxyFix
from urllib.parse import urlparse
import secrets

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.secret_key = os.environ.get("SESSION_SECRET", secrets.token_hex(16))
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User
from forms import LoginForm, RegistrationForm, SettingsForm

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if current_user.is_authenticated:
        g.theme = current_user.theme
        g.language = current_user.language
    else:
        g.theme = session.get('theme', 'light')
        g.language = session.get('language', 'en')

@app.route('/')
def index():
    return render_template('index.html', title='DiscoBots - Home')

@app.route('/discord')
def discord():
    return render_template('discord.html', title='DiscoBots - Join Our Discord')

@app.route('/terms')
def terms():
    return render_template('terms.html', title='DiscoBots - Terms & Privacy')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.theme = form.theme.data
        current_user.language = form.language.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.theme.data = current_user.theme
        form.language.data = current_user.language
    return render_template('settings.html', title='Settings', form=form)

@app.route('/set_language/<language>')
def set_language(language):
    if language not in ['en', 'fr']:
        language = 'en'
    if current_user.is_authenticated:
        current_user.language = language
        db.session.commit()
    else:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))

@app.route('/set_theme/<theme>')
def set_theme(theme):
    if theme not in ['light', 'dark']:
        theme = 'light'
    if current_user.is_authenticated:
        current_user.theme = theme
        db.session.commit()
    else:
        session['theme'] = theme
    return redirect(request.referrer or url_for('index'))

@app.route('/create-checkout-session', methods=['GET', 'POST'])
def create_checkout_session():
    # Set Stripe API key from environment variable
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

    # Get domain for success and cancel URLs
    domain_url = request.host_url.rstrip('/')
    
    try:
        # Create new Checkout Session for the order using existing product
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 599,  # $5.99 in cents
                        'product': 'prod_S5lpY8QkDBwJhx',  # Using the specific product ID
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=domain_url + url_for('checkout_success'),
            cancel_url=domain_url + url_for('checkout_cancel'),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        app.logger.error(f"Error creating checkout session: {str(e)}")
        flash('An error occurred while processing your payment. Please try again.')
        return redirect(url_for('index'))

@app.route('/checkout/success')
def checkout_success():
    return render_template('checkout_success.html', title='Payment Successful')

@app.route('/checkout/cancel')
def checkout_cancel():
    return render_template('checkout_cancel.html', title='Payment Cancelled')

with app.app_context():
    db.create_all()