"""
DiscoBots.fr - All-in-One File
This file contains all components of the DiscoBots.fr website:
- Flask application
- Database models
- Form definitions
- HTML templates (as strings)
- CSS styles (as strings)
- JavaScript (as strings)

Requirements:
Flask==2.3.3
flask-login==0.6.2
flask-sqlalchemy==3.1.1
flask-wtf==1.1.1
email-validator==2.0.0
psycopg2-binary==2.9.9
gunicorn==23.0.0
requests==2.31.0
stripe==7.2.0
werkzeug==2.3.7
wtforms==3.0.1
sqlalchemy==2.0.21

To run:
1. Install dependencies: pip install -r requirements.txt
2. Set environment variables:
   - DATABASE_URL: PostgreSQL connection string
   - STRIPE_SECRET_KEY: Your Stripe secret key
   - SESSION_SECRET: Random string for Flask session encryption
3. Run: python discobots_all_in_one.py
"""

import os
from datetime import datetime
from flask import Flask, render_template_string, url_for, flash, redirect, request, g, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import stripe

# ==================
# DATABASE SETUP
# ==================

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# ==================
# FLASK APP SETUP
# ==================

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db.init_app(app)

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configure Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# ==================
# DATABASE MODELS
# ==================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    theme = db.Column(db.String(20), default='light')
    language = db.Column(db.String(10), default='en')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ==================
# FORMS
# ==================

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class SettingsForm(FlaskForm):
    theme = SelectField('Theme', choices=[('light', 'White'), ('dark', 'Black')])
    language = SelectField('Language', choices=[('en', 'English'), ('fr', 'Français')])
    submit = SubmitField('Save Settings')

# ==================
# LOGIN MANAGER
# ==================

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))

# ==================
# UTILITY FUNCTIONS
# ==================

@app.before_request
def before_request():
    g.user = current_user
    if current_user.is_authenticated:
        g.theme = current_user.theme
        g.language = current_user.language
    else:
        g.theme = session.get('theme', 'light')
        g.language = session.get('language', 'en')

# ==================
# ROUTES
# ==================

@app.route('/')
def index():
    return render_template_string(TEMPLATE_INDEX)

@app.route('/discord')
def discord():
    return render_template_string(TEMPLATE_DISCORD)

@app.route('/terms')
def terms():
    return render_template_string(TEMPLATE_TERMS)

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
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('index')
        return redirect(next_page)
    return render_template_string(TEMPLATE_LOGIN, form=form)

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
    return render_template_string(TEMPLATE_REGISTER, form=form)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if request.method == 'GET':
        form.theme.data = current_user.theme
        form.language.data = current_user.language
    if form.validate_on_submit():
        current_user.theme = form.theme.data
        current_user.language = form.language.data
        db.session.commit()
        session['theme'] = current_user.theme
        session['language'] = current_user.language
        flash('Your settings have been updated.')
        return redirect(url_for('settings'))
    return render_template_string(TEMPLATE_SETTINGS, form=form)

@app.route('/set_language/<language>')
def set_language(language):
    if language in ['en', 'fr']:
        if current_user.is_authenticated:
            current_user.language = language
            db.session.commit()
        session['language'] = language
    return redirect(request.referrer or url_for('index'))

@app.route('/set_theme/<theme>')
def set_theme(theme):
    if theme in ['light', 'dark']:
        if current_user.is_authenticated:
            current_user.theme = theme
            db.session.commit()
        session['theme'] = theme
    return redirect(request.referrer or url_for('index'))

@app.route('/create-checkout-session')
def create_checkout_session():
    try:
        # The product ID for DiscoBots Standard plan
        product_id = "prod_S5lpY8QkDBwJhx"
        
        # Apply discount voucher if provided
        voucher = request.args.get('voucher')
        discount_code = None
        
        if voucher == 'Uflvb62d':
            # 30% discount coupon
            discount_code = 'Uflvb62d'
            
        domain_url = request.host_url.rstrip('/')
        
        # Create line items
        line_items = [{
            'price': product_id,
            'quantity': 1,
        }]
        
        # Create checkout session
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=domain_url + url_for('checkout_success'),
            cancel_url=domain_url + url_for('checkout_cancel'),
            discounts=[{'coupon': discount_code}] if discount_code else [],
        )
        
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e)

@app.route('/checkout-success')
def checkout_success():
    return render_template_string(TEMPLATE_CHECKOUT_SUCCESS)

@app.route('/checkout-cancel')
def checkout_cancel():
    return render_template_string(TEMPLATE_CHECKOUT_CANCEL)

# ==================
# HTML TEMPLATES
# ==================

TEMPLATE_BASE = """
<!DOCTYPE html>
<html lang="{{ g.language }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DiscoBots.fr - {% block title %}{% endblock %}</title>
    <style>{{ css_styles }}</style>
    <link rel="icon" href="data:image/png;base64,{{ favicon_data }}">
</head>
<body class="{{ g.theme }}">
    <canvas id="particles-js"></canvas>
    
    <header>
        <div class="container">
            <div class="logo">
                <a href="{{ url_for('index') }}">
                    <img src="data:image/png;base64,{{ logo_data }}" alt="DiscoBots.fr">
                </a>
            </div>
            <nav>
                <ul>
                    <li><a href="{{ url_for('index') }}">{% if g.language == 'fr' %}Accueil{% else %}Home{% endif %}</a></li>
                    <li><a href="{{ url_for('discord') }}">Discord</a></li>
                    <li><a href="{{ url_for('terms') }}">{% if g.language == 'fr' %}Conditions{% else %}Terms{% endif %}</a></li>
                    {% if current_user.is_authenticated %}
                    <li><a href="{{ url_for('settings') }}">{% if g.language == 'fr' %}Paramètres{% else %}Settings{% endif %}</a></li>
                    <li><a href="{{ url_for('logout') }}">{% if g.language == 'fr' %}Déconnexion{% else %}Logout{% endif %}</a></li>
                    {% else %}
                    <li><a href="{{ url_for('login') }}">{% if g.language == 'fr' %}Connexion{% else %}Login{% endif %}</a></li>
                    <li><a href="{{ url_for('register') }}">{% if g.language == 'fr' %}S'inscrire{% else %}Register{% endif %}</a></li>
                    {% endif %}
                </ul>
            </nav>
            <div class="theme-toggle">
                <a href="{{ url_for('set_theme', theme='light') }}" class="theme-btn {% if g.theme == 'light' %}active{% endif %}">☀️</a>
                <a href="{{ url_for('set_theme', theme='dark') }}" class="theme-btn {% if g.theme == 'dark' %}active{% endif %}">🌙</a>
            </div>
            <div class="language-toggle">
                <a href="{{ url_for('set_language', language='en') }}" class="lang-btn {% if g.language == 'en' %}active{% endif %}">🇬🇧</a>
                <a href="{{ url_for('set_language', language='fr') }}" class="lang-btn {% if g.language == 'fr' %}active{% endif %}">🇫🇷</a>
            </div>
        </div>
    </header>
    
    <main>
        <div class="container">
            {% with messages = get_flashed_messages() %}
            {% if messages %}
            <div class="flash-messages">
                {% for message in messages %}
                <div class="flash-message">{{ message }}</div>
                {% endfor %}
            </div>
            {% endif %}
            {% endwith %}
            
            {% if current_user.is_authenticated %}
            <div class="user-greeting">
                {% if g.language == 'fr' %}Bonjour{% else %}Hello{% endif %} {{ current_user.username }}!
            </div>
            {% endif %}
            
            {% block content %}{% endblock %}
        </div>
    </main>
    
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-logo">
                    <img src="data:image/png;base64,{{ logo_data }}" alt="DiscoBots.fr">
                </div>
                <div class="footer-links">
                    <ul>
                        <li><a href="{{ url_for('index') }}">{% if g.language == 'fr' %}Accueil{% else %}Home{% endif %}</a></li>
                        <li><a href="{{ url_for('discord') }}">Discord</a></li>
                        <li><a href="{{ url_for('terms') }}">{% if g.language == 'fr' %}Conditions{% else %}Terms{% endif %}</a></li>
                        <li><a href="#pricing">{% if g.language == 'fr' %}Tarification{% else %}Pricing{% endif %}</a></li>
                        <li><a href="#faq">FAQ</a></li>
                    </ul>
                </div>
                <div class="footer-contact">
                    <p>{% if g.language == 'fr' %}Contactez-nous{% else %}Contact Us{% endif %}</p>
                    <a href="mailto:discobots.com@gmail.com">discobots.com@gmail.com</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 DiscoBots.fr. {% if g.language == 'fr' %}Tous droits réservés.{% else %}All rights reserved.{% endif %}</p>
            </div>
        </div>
    </footer>
    
    <script>{{ js_particles }}</script>
    <script>{{ js_main }}</script>
</body>
</html>
"""

TEMPLATE_INDEX = """
{% extends "base.html" %}

{% block title %}{% if g.language == 'fr' %}Accueil{% else %}Home{% endif %}{% endblock %}

{% block content %}
<section class="home-hero">
    <div class="hero-content">
        <h1>{% if g.language == 'fr' %}Bienvenue sur DiscoBots.fr{% else %}Welcome to DiscoBots.fr{% endif %}</h1>
        <p>
            {% if g.language == 'fr' %}
            Découvrez un bot Discord puissant et facile à utiliser qui améliorera votre serveur avec des fonctionnalités étonnantes.
            {% else %}
            Discover a powerful and easy-to-use Discord bot that will enhance your server with amazing features.
            {% endif %}
        </p>
        <a href="{{ url_for('discord') }}" class="cta-button">
            {% if g.language == 'fr' %}Ajouter à Discord{% else %}Add to Discord{% endif %}
        </a>
    </div>
</section>

<section class="features">
    <h2>{% if g.language == 'fr' %}Fonctionnalités{% else %}Features{% endif %}</h2>
    <div class="feature-grid">
        <div class="feature-card">
            <h3>{% if g.language == 'fr' %}Modération{% else %}Moderation{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                Gardez votre serveur propre et sécurisé avec des outils de modération avancés.
                {% else %}
                Keep your server clean and secure with advanced moderation tools.
                {% endif %}
            </p>
        </div>
        <div class="feature-card">
            <h3>{% if g.language == 'fr' %}Musique{% else %}Music{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                Jouez de la musique de haute qualité depuis diverses plateformes.
                {% else %}
                Play high-quality music from various platforms.
                {% endif %}
            </p>
        </div>
        <div class="feature-card">
            <h3>{% if g.language == 'fr' %}Personnalisation{% else %}Customization{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                Adaptez le bot à votre serveur avec des options de personnalisation étendues.
                {% else %}
                Tailor the bot to your server with extensive customization options.
                {% endif %}
            </p>
        </div>
        <div class="feature-card">
            <h3>{% if g.language == 'fr' %}Économie{% else %}Economy{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                Créez un système économique engageant pour votre communauté.
                {% else %}
                Create an engaging economy system for your community.
                {% endif %}
            </p>
        </div>
    </div>
</section>

<section class="pricing" id="pricing">
    <h2>{% if g.language == 'fr' %}Tarification{% else %}Pricing{% endif %}</h2>
    
    <div class="promotion-banner">
        {% if g.language == 'fr' %}
        <span>🔥 Offre Spéciale: Utilisez le code <span class="coupon-code">DISCO30</span> pour obtenir 30% de réduction! 🔥</span>
        {% else %}
        <span>🔥 Special Offer: Use code <span class="coupon-code">DISCO30</span> for 30% off! 🔥</span>
        {% endif %}
    </div>
    
    <div class="pricing-grid">
        <div class="pricing-card">
            <h3>{% if g.language == 'fr' %}Standard{% else %}Standard{% endif %}</h3>
            <div class="price">$5.99</div>
            <ul class="pricing-features">
                <li>{% if g.language == 'fr' %}Accès complet aux fonctionnalités{% else %}Full access to all features{% endif %}</li>
                <li>{% if g.language == 'fr' %}Support prioritaire{% else %}Priority support{% endif %}</li>
                <li>{% if g.language == 'fr' %}Jusqu'à 10 serveurs{% else %}Up to 10 servers{% endif %}</li>
            </ul>
            <a href="{{ url_for('create_checkout_session') }}" class="cta-button">
                {% if g.language == 'fr' %}Acheter maintenant{% else %}Buy Now{% endif %}
            </a>
            <div style="margin-top: 10px; font-size: 0.9em;">
                <a href="{{ url_for('create_checkout_session', voucher='Uflvb62d') }}" style="text-decoration: underline;">
                    {% if g.language == 'fr' %}Utiliser le code promotion{% else %}Use discount code{% endif %}
                </a>
            </div>
        </div>
        <div class="pricing-card featured">
            <h3>{% if g.language == 'fr' %}Personnalisé{% else %}Custom{% endif %}</h3>
            <div class="price">{% if g.language == 'fr' %}Contactez-nous{% else %}Contact Us{% endif %}</div>
            <ul class="pricing-features">
                <li>{% if g.language == 'fr' %}Fonctionnalités personnalisées{% else %}Custom features{% endif %}</li>
                <li>{% if g.language == 'fr' %}Support dédié 24/7{% else %}24/7 Dedicated support{% endif %}</li>
                <li>{% if g.language == 'fr' %}Serveurs illimités{% else %}Unlimited servers{% endif %}</li>
            </ul>
            <a href="mailto:discobots.com@gmail.com" class="cta-button secondary">
                {% if g.language == 'fr' %}Contactez-nous{% else %}Contact Us{% endif %}
            </a>
        </div>
    </div>
</section>

<section class="how-to-use" id="how-to-use">
    <h2>{% if g.language == 'fr' %}Comment utiliser{% else %}How to Use{% endif %}</h2>
    <div class="steps">
        <div class="step">
            <div class="step-number">1</div>
            <h3>{% if g.language == 'fr' %}Inviter le bot{% else %}Invite the Bot{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                Cliquez sur le bouton "Ajouter à Discord" pour inviter le bot sur votre serveur.
                {% else %}
                Click the "Add to Discord" button to invite the bot to your server.
                {% endif %}
            </p>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <h3>{% if g.language == 'fr' %}Configuration{% else %}Configuration{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                Utilisez la commande !setup pour configurer le bot selon vos préférences.
                {% else %}
                Use the !setup command to configure the bot according to your preferences.
                {% endif %}
            </p>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <h3>{% if g.language == 'fr' %}Profitez{% else %}Enjoy{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                Votre bot est maintenant prêt à l'emploi ! Utilisez !help pour voir toutes les commandes.
                {% else %}
                Your bot is now ready to use! Type !help to see all available commands.
                {% endif %}
            </p>
        </div>
    </div>
</section>

<section class="faq" id="faq">
    <h2>{% if g.language == 'fr' %}Foire Aux Questions{% else %}Frequently Asked Questions{% endif %}</h2>
    <div class="faq-container">
        <div class="faq-item">
            <div class="faq-question">
                {% if g.language == 'fr' %}
                Est-ce que je peux utiliser le bot gratuitement ?
                {% else %}
                Can I use the bot for free?
                {% endif %}
            </div>
            <div class="faq-answer">
                {% if g.language == 'fr' %}
                Oui, vous pouvez utiliser la version de base gratuitement, mais avec des fonctionnalités limitées. Pour un accès complet, envisagez notre forfait Standard à $5.99.
                {% else %}
                Yes, you can use the basic version for free, but with limited features. For full access, consider our Standard plan at $5.99.
                {% endif %}
            </div>
        </div>
        <div class="faq-item">
            <div class="faq-question">
                {% if g.language == 'fr' %}
                Comment puis-je obtenir de l'aide si j'ai un problème ?
                {% else %}
                How can I get help if I have an issue?
                {% endif %}
            </div>
            <div class="faq-answer">
                {% if g.language == 'fr' %}
                Rejoignez notre serveur Discord pour obtenir de l'aide de notre équipe de support ou contactez-nous directement à discobots.com@gmail.com.
                {% else %}
                Join our Discord server to get help from our support team, or contact us directly at discobots.com@gmail.com.
                {% endif %}
            </div>
        </div>
        <div class="faq-item">
            <div class="faq-question">
                {% if g.language == 'fr' %}
                Puis-je personnaliser les commandes du bot ?
                {% else %}
                Can I customize the bot's commands?
                {% endif %}
            </div>
            <div class="faq-answer">
                {% if g.language == 'fr' %}
                Oui, notre bot offre de nombreuses options de personnalisation. Avec le forfait Standard, vous pouvez personnaliser davantage de commandes et de fonctionnalités.
                {% else %}
                Yes, our bot offers many customization options. With the Standard plan, you can customize even more commands and features.
                {% endif %}
            </div>
        </div>
        <div class="faq-item">
            <div class="faq-question">
                {% if g.language == 'fr' %}
                Le bot fonctionne-t-il sur mobile ?
                {% else %}
                Does the bot work on mobile?
                {% endif %}
            </div>
            <div class="faq-answer">
                {% if g.language == 'fr' %}
                Oui, notre bot fonctionne parfaitement sur toutes les plateformes où Discord est disponible, y compris les appareils mobiles.
                {% else %}
                Yes, our bot works seamlessly on all platforms where Discord is available, including mobile devices.
                {% endif %}
            </div>
        </div>
    </div>
</section>

<section class="special-offer-section">
    <h3>{% if g.language == 'fr' %}Offre exclusive pour les nouveaux utilisateurs{% else %}Exclusive Offer for New Users{% endif %}</h3>
    <p>
        {% if g.language == 'fr' %}
        Inscrivez-vous aujourd'hui et obtenez un mois d'essai gratuit du plan Standard ! Pas besoin de carte de crédit.
        {% else %}
        Sign up today and get a free 1-month trial of the Standard plan! No credit card required.
        {% endif %}
    </p>
    <div class="countdown-timer">
        <span id="countdown">48:00:00</span>
    </div>
    <a href="{{ url_for('register') }}" class="cta-button">
        {% if g.language == 'fr' %}S'inscrire maintenant{% else %}Sign Up Now{% endif %}
    </a>
</section>

<section class="testimonials">
    <h2>{% if g.language == 'fr' %}Ce que les utilisateurs disent{% else %}What Users Say{% endif %}</h2>
    <div class="testimonial-slider">
        <div class="testimonial">
            <p>"{% if g.language == 'fr' %}Le meilleur bot que j'ai utilisé pour mon serveur ! Les fonctionnalités de modération sont vraiment impressionnantes.{% else %}The best bot I've used for my server! The moderation features are really impressive.{% endif %}"</p>
            <cite>- Neporrex</cite>
        </div>
        <div class="testimonial">
            <p>"{% if g.language == 'fr' %}La qualité de la musique est excellente, et le bot est très stable. Hautement recommandé !{% else %}The music quality is excellent, and the bot is very stable. Highly recommended!{% endif %}"</p>
            <cite>- Belunoobs</cite>
        </div>
    </div>
</section>
{% endblock %}
"""

TEMPLATE_DISCORD = """
{% extends "base.html" %}

{% block title %}Discord{% endblock %}

{% block content %}
<section class="discord-section">
    <div class="discord-content">
        <h1>{% if g.language == 'fr' %}Rejoignez notre serveur Discord{% else %}Join Our Discord Server{% endif %}</h1>
        <p>
            {% if g.language == 'fr' %}
            Rejoignez notre communauté Discord pour obtenir de l'aide, discuter avec d'autres utilisateurs, et rester informé des dernières mises à jour de DiscoBots.
            {% else %}
            Join our Discord community to get help, chat with other users, and stay updated on the latest DiscoBots updates.
            {% endif %}
        </p>
        
        <div class="discord-invite">
            <a href="https://discord.gg/XBY893MsgC" target="_blank" class="discord-button">
                {% if g.language == 'fr' %}Rejoindre le serveur Discord{% else %}Join Discord Server{% endif %}
            </a>
        </div>
        
        <div class="discord-benefits">
            <h2>{% if g.language == 'fr' %}Avantages{% else %}Benefits{% endif %}</h2>
            <ul>
                <li>
                    {% if g.language == 'fr' %}
                    Support direct et rapide de notre équipe
                    {% else %}
                    Direct and quick support from our team
                    {% endif %}
                </li>
                <li>
                    {% if g.language == 'fr' %}
                    Accès anticipé aux nouvelles fonctionnalités
                    {% else %}
                    Early access to new features
                    {% endif %}
                </li>
                <li>
                    {% if g.language == 'fr' %}
                    Rencontrez d'autres administrateurs de serveurs
                    {% else %}
                    Meet other server administrators
                    {% endif %}
                </li>
                <li>
                    {% if g.language == 'fr' %}
                    Participez à des événements exclusifs
                    {% else %}
                    Participate in exclusive events
                    {% endif %}
                </li>
            </ul>
        </div>
    </div>
    
    <div class="discord-add-bot">
        <h2>{% if g.language == 'fr' %}Ajouter le bot à votre serveur{% else %}Add the Bot to Your Server{% endif %}</h2>
        <p>
            {% if g.language == 'fr' %}
            Prêt à améliorer votre serveur avec DiscoBots ? Cliquez sur le bouton ci-dessous pour ajouter le bot à votre serveur Discord.
            {% else %}
            Ready to enhance your server with DiscoBots? Click the button below to add the bot to your Discord server.
            {% endif %}
        </p>
        <a href="https://discord.com/oauth2/authorize?client_id=123456789012345678&scope=bot&permissions=8" target="_blank" class="bot-add-button">
            {% if g.language == 'fr' %}Ajouter le bot{% else %}Add Bot{% endif %}
        </a>
    </div>
</section>
{% endblock %}
"""

TEMPLATE_TERMS = """
{% extends "base.html" %}

{% block title %}{% if g.language == 'fr' %}Conditions{% else %}Terms{% endif %}{% endblock %}

{% block content %}
<section class="terms-section">
    <h1>{% if g.language == 'fr' %}Conditions d'utilisation & Politique de confidentialité{% else %}Terms of Service & Privacy Policy{% endif %}</h1>
    
    <div class="terms-content">
        <div class="terms-section">
            <h2>{% if g.language == 'fr' %}Conditions d'utilisation{% else %}Terms of Service{% endif %}</h2>
            <p>
                {% if g.language == 'fr' %}
                Dernière mise à jour : 1 avril 2024
                {% else %}
                Last updated: April 1, 2024
                {% endif %}
            </p>
            
            <h3>{% if g.language == 'fr' %}1. Acceptation des conditions{% else %}1. Acceptance of Terms{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                En utilisant DiscoBots.fr et nos services de bot Discord, vous acceptez d'être lié par ces conditions. Si vous n'acceptez pas ces conditions, veuillez ne pas utiliser nos services.
                {% else %}
                By using DiscoBots.fr and our Discord bot services, you agree to be bound by these terms. If you do not agree to these terms, please do not use our services.
                {% endif %}
            </p>
            
            <h3>{% if g.language == 'fr' %}2. Description du service{% else %}2. Service Description{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                DiscoBots.fr fournit un bot Discord avec diverses fonctionnalités pour les serveurs Discord. Nous proposons une version gratuite avec des fonctionnalités limitées et des plans payants avec des fonctionnalités supplémentaires.
                {% else %}
                DiscoBots.fr provides a Discord bot with various features for Discord servers. We offer a free version with limited features and paid plans with additional features.
                {% endif %}
            </p>
            
            <h3>{% if g.language == 'fr' %}3. Utilisation acceptable{% else %}3. Acceptable Use{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                Vous acceptez de ne pas utiliser notre bot pour violer les conditions de service de Discord, promouvoir du contenu illégal, ou harceler d'autres utilisateurs. Nous nous réservons le droit de résilier l'accès à notre service pour toute utilisation abusive.
                {% else %}
                You agree not to use our bot to violate Discord's terms of service, promote illegal content, or harass other users. We reserve the right to terminate access to our service for any abusive usage.
                {% endif %}
            </p>
            
            <h3>{% if g.language == 'fr' %}4. Paiements et remboursements{% else %}4. Payments and Refunds{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                Tous les paiements sont traités via Stripe. Les remboursements peuvent être demandés dans les 7 jours suivant l'achat si le service ne fonctionne pas comme prévu. Contactez-nous à discobots.com@gmail.com pour toute demande de remboursement.
                {% else %}
                All payments are processed through Stripe. Refunds may be requested within 7 days of purchase if the service does not function as expected. Contact us at discobots.com@gmail.com for any refund requests.
                {% endif %}
            </p>
        </div>
        
        <div class="privacy-section">
            <h2>{% if g.language == 'fr' %}Politique de confidentialité{% else %}Privacy Policy{% endif %}</h2>
            <p>
                {% if g.language == 'fr' %}
                Dernière mise à jour : 1 avril 2024
                {% else %}
                Last updated: April 1, 2024
                {% endif %}
            </p>
            
            <h3>{% if g.language == 'fr' %}1. Informations que nous collectons{% else %}1. Information We Collect{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                Nous collectons les informations suivantes :
                <ul>
                    <li>Nom d'utilisateur et courriel lors de l'inscription</li>
                    <li>Préférences (thème, langue)</li>
                    <li>ID de serveur Discord lorsque le bot est ajouté</li>
                    <li>Commandes utilisées avec le bot</li>
                </ul>
                {% else %}
                We collect the following information:
                <ul>
                    <li>Username and email during registration</li>
                    <li>Preferences (theme, language)</li>
                    <li>Discord server ID when the bot is added</li>
                    <li>Commands used with the bot</li>
                </ul>
                {% endif %}
            </p>
            
            <h3>{% if g.language == 'fr' %}2. Comment nous utilisons vos informations{% else %}2. How We Use Your Information{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                Nous utilisons vos informations pour :
                <ul>
                    <li>Fournir et améliorer nos services</li>
                    <li>Communiquer avec vous concernant votre compte</li>
                    <li>Personnaliser votre expérience</li>
                    <li>Traiter les paiements</li>
                </ul>
                {% else %}
                We use your information to:
                <ul>
                    <li>Provide and improve our services</li>
                    <li>Communicate with you regarding your account</li>
                    <li>Personalize your experience</li>
                    <li>Process payments</li>
                </ul>
                {% endif %}
            </p>
            
            <h3>{% if g.language == 'fr' %}3. Partage d'informations{% else %}3. Information Sharing{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                Nous ne vendons pas vos informations personnelles. Nous pouvons partager vos informations avec des fournisseurs de services tiers qui nous aident à fournir nos services (comme Stripe pour les paiements).
                {% else %}
                We do not sell your personal information. We may share your information with third-party service providers who help us deliver our services (such as Stripe for payments).
                {% endif %}
            </p>
            
            <h3>{% if g.language == 'fr' %}4. Vos droits{% else %}4. Your Rights{% endif %}</h3>
            <p>
                {% if g.language == 'fr' %}
                Vous avez le droit d'accéder, de corriger, ou de supprimer vos informations personnelles. Pour exercer ces droits, contactez-nous à discobots.com@gmail.com.
                {% else %}
                You have the right to access, correct, or delete your personal information. To exercise these rights, contact us at discobots.com@gmail.com.
                {% endif %}
            </p>
        </div>
        
        <div class="contact-section">
            <h2>{% if g.language == 'fr' %}Contact{% else %}Contact{% endif %}</h2>
            <p>
                {% if g.language == 'fr' %}
                Si vous avez des questions concernant ces conditions ou notre politique de confidentialité, veuillez nous contacter à discobots.com@gmail.com.
                {% else %}
                If you have any questions regarding these terms or our privacy policy, please contact us at discobots.com@gmail.com.
                {% endif %}
            </p>
        </div>
    </div>
</section>
{% endblock %}
"""

TEMPLATE_LOGIN = """
{% extends "base.html" %}

{% block title %}{% if g.language == 'fr' %}Connexion{% else %}Login{% endif %}{% endblock %}

{% block content %}
<section class="auth-section">
    <h1>{% if g.language == 'fr' %}Connexion{% else %}Login{% endif %}</h1>
    <div class="auth-container">
        <form method="post" action="" novalidate>
            {{ form.hidden_tag() }}
            <div class="form-group">
                {{ form.username.label }}
                {{ form.username(size=32, class="form-control") }}
                {% for error in form.username.errors %}
                <span class="error">{{ error }}</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.password.label }}
                {{ form.password(size=32, class="form-control") }}
                {% for error in form.password.errors %}
                <span class="error">{{ error }}</span>
                {% endfor %}
            </div>
            <div class="form-group checkbox">
                {{ form.remember_me() }}
                {{ form.remember_me.label }}
            </div>
            <div class="form-group">
                {{ form.submit(class="cta-button") }}
            </div>
        </form>
        <div class="auth-links">
            <p>
                {% if g.language == 'fr' %}
                Besoin d'un compte ? <a href="{{ url_for('register') }}">S'inscrire</a>
                {% else %}
                Need an account? <a href="{{ url_for('register') }}">Register</a>
                {% endif %}
            </p>
        </div>
    </div>
</section>
{% endblock %}
"""

TEMPLATE_REGISTER = """
{% extends "base.html" %}

{% block title %}{% if g.language == 'fr' %}S'inscrire{% else %}Register{% endif %}{% endblock %}

{% block content %}
<section class="auth-section">
    <h1>{% if g.language == 'fr' %}S'inscrire{% else %}Register{% endif %}</h1>
    <div class="auth-container">
        <form method="post" action="" novalidate>
            {{ form.hidden_tag() }}
            <div class="form-group">
                {{ form.username.label }}
                {{ form.username(size=32, class="form-control") }}
                {% for error in form.username.errors %}
                <span class="error">{{ error }}</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.email.label }}
                {{ form.email(size=64, class="form-control") }}
                {% for error in form.email.errors %}
                <span class="error">{{ error }}</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.password.label }}
                {{ form.password(size=32, class="form-control") }}
                {% for error in form.password.errors %}
                <span class="error">{{ error }}</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.password2.label }}
                {{ form.password2(size=32, class="form-control") }}
                {% for error in form.password2.errors %}
                <span class="error">{{ error }}</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.submit(class="cta-button") }}
            </div>
        </form>
        <div class="auth-links">
            <p>
                {% if g.language == 'fr' %}
                Déjà inscrit ? <a href="{{ url_for('login') }}">Connexion</a>
                {% else %}
                Already registered? <a href="{{ url_for('login') }}">Login</a>
                {% endif %}
            </p>
        </div>
    </div>
</section>
{% endblock %}
"""

TEMPLATE_SETTINGS = """
{% extends "base.html" %}

{% block title %}{% if g.language == 'fr' %}Paramètres{% else %}Settings{% endif %}{% endblock %}

{% block content %}
<section class="settings-section">
    <h1>{% if g.language == 'fr' %}Paramètres{% else %}Settings{% endif %}</h1>
    <div class="settings-container">
        <form method="post" action="" novalidate>
            {{ form.hidden_tag() }}
            <div class="form-group">
                {{ form.theme.label }}
                {{ form.theme(class="form-control") }}
            </div>
            <div class="form-group">
                {{ form.language.label }}
                {{ form.language(class="form-control") }}
            </div>
            <div class="form-group">
                {{ form.submit(class="cta-button") }}
            </div>
        </form>
    </div>
</section>
{% endblock %}
"""

TEMPLATE_CHECKOUT_SUCCESS = """
{% extends "base.html" %}

{% block title %}{% if g.language == 'fr' %}Paiement réussi{% else %}Payment Successful{% endif %}{% endblock %}

{% block content %}
<section class="checkout-success">
    <div class="success-container">
        <h1>{% if g.language == 'fr' %}Paiement réussi !{% else %}Payment Successful!{% endif %}</h1>
        <p>
            {% if g.language == 'fr' %}
            Merci pour votre achat ! Votre paiement a été traité avec succès.
            {% else %}
            Thank you for your purchase! Your payment has been successfully processed.
            {% endif %}
        </p>
        <div class="next-steps">
            <h2>{% if g.language == 'fr' %}Prochaines étapes{% else %}Next Steps{% endif %}</h2>
            <p>
                {% if g.language == 'fr' %}
                1. Rejoignez notre serveur Discord si ce n'est pas déjà fait.<br>
                2. Utilisez la commande !activate pour activer votre abonnement.<br>
                3. Profitez de toutes les fonctionnalités de DiscoBots !
                {% else %}
                1. Join our Discord server if you haven't already.<br>
                2. Use the !activate command to activate your subscription.<br>
                3. Enjoy all the features of DiscoBots!
                {% endif %}
            </p>
        </div>
        <a href="{{ url_for('index') }}" class="cta-button">
            {% if g.language == 'fr' %}Retour à l'accueil{% else %}Back to Home{% endif %}
        </a>
    </div>
</section>
{% endblock %}
"""

TEMPLATE_CHECKOUT_CANCEL = """
{% extends "base.html" %}

{% block title %}{% if g.language == 'fr' %}Paiement annulé{% else %}Payment Cancelled{% endif %}{% endblock %}

{% block content %}
<section class="checkout-cancel">
    <div class="cancel-container">
        <h1>{% if g.language == 'fr' %}Paiement annulé{% else %}Payment Cancelled{% endif %}</h1>
        <p>
            {% if g.language == 'fr' %}
            Votre paiement a été annulé. Aucun montant n'a été débité de votre compte.
            {% else %}
            Your payment has been cancelled. No charge has been made to your account.
            {% endif %}
        </p>
        <p>
            {% if g.language == 'fr' %}
            Si vous avez des questions ou avez rencontré des problèmes lors du processus de paiement, n'hésitez pas à nous contacter à discobots.com@gmail.com.
            {% else %}
            If you have any questions or experienced any issues with the payment process, please feel free to contact us at discobots.com@gmail.com.
            {% endif %}
        </p>
        <a href="{{ url_for('index') }}" class="cta-button">
            {% if g.language == 'fr' %}Retour à l'accueil{% else %}Back to Home{% endif %}
        </a>
    </div>
</section>
{% endblock %}
"""

# ==================
# CSS STYLES
# ==================

css_styles = """
/* Global Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    position: relative;
}

body.light {
    background-color: #ffffff;
    color: #333333;
}

body.dark {
    background-color: #1a1a1a;
    color: #f5f5f5;
}

canvas#particles-js {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
}

a {
    text-decoration: none;
    transition: all 0.3s ease;
}

.light a {
    color: #3a3a3a;
}

.dark a {
    color: #d6d6d6;
}

a:hover {
    opacity: 0.8;
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
header {
    padding: 20px 0;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.light header {
    background-color: rgba(255, 255, 255, 0.95);
    border-bottom-color: rgba(0, 0, 0, 0.1);
}

.dark header {
    background-color: rgba(26, 26, 26, 0.95);
    border-bottom-color: rgba(255, 255, 255, 0.1);
}

header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo img {
    height: 50px;
}

nav ul {
    display: flex;
    list-style: none;
}

nav ul li {
    margin-left: 20px;
}

nav ul li a {
    font-weight: 500;
    padding: 5px 10px;
    border-radius: 4px;
}

nav ul li a:hover {
    background-color: rgba(0, 0, 0, 0.05);
}

.dark nav ul li a:hover {
    background-color: rgba(255, 255, 255, 0.05);
}

.theme-toggle,
.language-toggle {
    display: flex;
    align-items: center;
}

.theme-btn,
.lang-btn {
    margin-left: 10px;
    padding: 5px;
    font-size: 18px;
    cursor: pointer;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.theme-btn.active,
.lang-btn.active {
    background-color: rgba(0, 0, 0, 0.1);
}

.dark .theme-btn.active,
.dark .lang-btn.active {
    background-color: rgba(255, 255, 255, 0.1);
}

/* Main Content */
main {
    flex: 1;
    padding: 40px 0;
}

.user-greeting {
    margin-bottom: 20px;
    padding: 10px;
    background-color: rgba(0, 0, 0, 0.05);
    border-radius: 4px;
    text-align: center;
}

.dark .user-greeting {
    background-color: rgba(255, 255, 255, 0.05);
}

.flash-messages {
    margin-bottom: 20px;
}

.flash-message {
    padding: 10px;
    border-radius: 4px;
    background-color: rgba(0, 0, 0, 0.05);
    margin-bottom: 10px;
}

.dark .flash-message {
    background-color: rgba(255, 255, 255, 0.05);
}

/* Hero Section */
.home-hero {
    text-align: center;
    padding: 80px 0;
}

.hero-content h1 {
    font-size: 2.5rem;
    margin-bottom: 20px;
}

.hero-content p {
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto 30px;
}

/* Features Section */
.features {
    padding: 60px 0;
    text-align: center;
}

.features h2 {
    font-size: 2rem;
    margin-bottom: 40px;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
}

.feature-card {
    padding: 30px;
    border-radius: 8px;
    transition: transform 0.3s ease;
}

.light .feature-card {
    background-color: rgba(0, 0, 0, 0.02);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.dark .feature-card {
    background-color: rgba(255, 255, 255, 0.02);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-card h3 {
    margin-bottom: 15px;
}

/* Pricing Section */
.pricing {
    padding: 60px 0;
    text-align: center;
}

.pricing h2 {
    font-size: 2rem;
    margin-bottom: 20px;
}

.promotion-banner {
    margin: 0 auto 40px;
    padding: 10px 20px;
    border-radius: 30px;
    display: inline-block;
    font-weight: bold;
    animation: pulse 2s infinite;
}

.light .promotion-banner {
    background-color: rgba(0, 0, 0, 0.05);
}

.dark .promotion-banner {
    background-color: rgba(255, 255, 255, 0.05);
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.2);
    }
    70% {
        box-shadow: 0 0 0 10px rgba(0, 0, 0, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
    }
}

.dark @keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.2);
    }
    70% {
        box-shadow: 0 0 0 10px rgba(255, 255, 255, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(255, 255, 255, 0);
    }
}

.coupon-code {
    font-family: monospace;
    font-weight: bold;
    padding: 3px 6px;
    border-radius: 4px;
}

.light .coupon-code {
    background-color: rgba(0, 0, 0, 0.1);
}

.dark .coupon-code {
    background-color: rgba(255, 255, 255, 0.1);
}

.pricing-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    max-width: 900px;
    margin: 0 auto;
}

.pricing-card {
    padding: 30px;
    border-radius: 8px;
    transition: transform 0.3s ease;
    display: flex;
    flex-direction: column;
}

.light .pricing-card {
    background-color: rgba(0, 0, 0, 0.02);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.dark .pricing-card {
    background-color: rgba(255, 255, 255, 0.02);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.pricing-card.featured {
    transform: scale(1.05);
}

.pricing-card h3 {
    font-size: 1.5rem;
    margin-bottom: 15px;
}

.price {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 20px;
}

.pricing-features {
    list-style: none;
    margin-bottom: 25px;
    flex-grow: 1;
}

.pricing-features li {
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.dark .pricing-features li {
    border-bottom-color: rgba(255, 255, 255, 0.05);
}

.pricing-features li:last-child {
    border-bottom: none;
}

/* How to Use Section */
.how-to-use {
    padding: 60px 0;
    text-align: center;
}

.how-to-use h2 {
    font-size: 2rem;
    margin-bottom: 40px;
}

.steps {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 30px;
}

.step {
    flex: 1;
    min-width: 250px;
    max-width: 300px;
    padding: 30px;
    border-radius: 8px;
    position: relative;
}

.light .step {
    background-color: rgba(0, 0, 0, 0.02);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.dark .step {
    background-color: rgba(255, 255, 255, 0.02);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.step-number {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin: 0 auto 20px;
}

.light .step-number {
    background-color: rgba(0, 0, 0, 0.1);
}

.dark .step-number {
    background-color: rgba(255, 255, 255, 0.1);
}

.step h3 {
    margin-bottom: 15px;
}

/* FAQ Section */
.faq {
    padding: 60px 0;
    text-align: center;
}

.faq h2 {
    font-size: 2rem;
    margin-bottom: 40px;
}

.faq-container {
    max-width: 800px;
    margin: 0 auto;
}

.faq-item {
    margin-bottom: 20px;
    text-align: left;
    border-radius: 8px;
    overflow: hidden;
}

.faq-question {
    padding: 15px 20px;
    font-weight: bold;
    cursor: pointer;
    position: relative;
}

.light .faq-question {
    background-color: rgba(0, 0, 0, 0.03);
}

.dark .faq-question {
    background-color: rgba(255, 255, 255, 0.03);
}

.faq-question:after {
    content: '+';
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 20px;
}

.faq-item.active .faq-question:after {
    content: '-';
}

.faq-answer {
    padding: 0 20px;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease, padding 0.3s ease;
}

.faq-item.active .faq-answer {
    padding: 20px;
    max-height: 1000px;
}

.light .faq-answer {
    background-color: rgba(0, 0, 0, 0.01);
}

.dark .faq-answer {
    background-color: rgba(255, 255, 255, 0.01);
}

/* Special Offer Section */
.special-offer-section {
    text-align: center;
    padding: 40px;
    margin: 60px auto;
    max-width: 800px;
    border-radius: 10px;
}

.light .special-offer-section {
    background-color: rgba(0, 0, 0, 0.02);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.dark .special-offer-section {
    background-color: rgba(255, 255, 255, 0.02);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.special-offer-section h3 {
    font-size: 1.8rem;
    margin-bottom: 20px;
}

.special-offer-section p {
    margin-bottom: 30px;
}

.countdown-timer {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 30px;
    font-family: monospace;
}

/* Testimonials Section */
.testimonials {
    padding: 60px 0;
    text-align: center;
}

.testimonials h2 {
    font-size: 2rem;
    margin-bottom: 40px;
}

.testimonial-slider {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 30px;
}

.testimonial {
    padding: 30px;
    border-radius: 8px;
    flex: 1;
    min-width: 300px;
}

.light .testimonial {
    background-color: rgba(0, 0, 0, 0.02);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.dark .testimonial {
    background-color: rgba(255, 255, 255, 0.02);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.testimonial p {
    font-style: italic;
    margin-bottom: 20px;
}

.testimonial cite {
    font-weight: bold;
}

/* Discord Page Styles */
.discord-section {
    padding: 60px 0;
    text-align: center;
}

.discord-content {
    max-width: 800px;
    margin: 0 auto 60px;
}

.discord-content h1 {
    font-size: 2.5rem;
    margin-bottom: 20px;
}

.discord-content p {
    margin-bottom: 30px;
}

.discord-invite {
    margin: 40px 0;
}

.discord-button {
    display: inline-block;
    padding: 15px 30px;
    font-size: 1.1rem;
    font-weight: bold;
    border-radius: 5px;
    text-transform: uppercase;
    letter-spacing: 1px;
    background-color: #5865F2;
    color: white !important;
    transition: background-color 0.3s ease;
}

.discord-button:hover {
    background-color: #4752c4;
    opacity: 1;
}

.discord-benefits {
    margin-top: 50px;
}

.discord-benefits h2 {
    font-size: 1.8rem;
    margin-bottom: 30px;
}

.discord-benefits ul {
    list-style: none;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

.discord-benefits li {
    padding: 20px;
    border-radius: 8px;
}

.light .discord-benefits li {
    background-color: rgba(0, 0, 0, 0.02);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.dark .discord-benefits li {
    background-color: rgba(255, 255, 255, 0.02);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.discord-add-bot {
    max-width: 800px;
    margin: 60px auto 0;
    padding: 40px;
    border-radius: 10px;
}

.light .discord-add-bot {
    background-color: rgba(0, 0, 0, 0.02);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.dark .discord-add-bot {
    background-color: rgba(255, 255, 255, 0.02);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.discord-add-bot h2 {
    font-size: 1.8rem;
    margin-bottom: 20px;
}

.discord-add-bot p {
    margin-bottom: 30px;
}

.bot-add-button {
    display: inline-block;
    padding: 12px 25px;
    font-weight: bold;
    border-radius: 5px;
    background-color: #5865F2;
    color: white !important;
    transition: background-color 0.3s ease;
}

.bot-add-button:hover {
    background-color: #4752c4;
    opacity: 1;
}

/* Terms Page Styles */
.terms-section {
    padding: 60px 0;
    max-width: 800px;
    margin: 0 auto;
}

.terms-section h1 {
    font-size: 2.2rem;
    margin-bottom: 40px;
    text-align: center;
}

.terms-section h2 {
    font-size: 1.8rem;
    margin: 40px 0 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.dark .terms-section h2 {
    border-bottom-color: rgba(255, 255, 255, 0.1);
}

.terms-section h3 {
    font-size: 1.4rem;
    margin: 30px 0 15px;
}

.terms-section p, .terms-section ul {
    margin-bottom: 20px;
}

.terms-section ul {
    padding-left: 20px;
}

.terms-section ul li {
    margin-bottom: 10px;
}

.contact-section {
    margin-top: 60px;
    padding-top: 30px;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.dark .contact-section {
    border-top-color: rgba(255, 255, 255, 0.1);
}

/* Auth Pages Styles */
.auth-section {
    padding: 60px 0;
    text-align: center;
}

.auth-section h1 {
    font-size: 2.2rem;
    margin-bottom: 40px;
}

.auth-container {
    max-width: 500px;
    margin: 0 auto;
    padding: 30px;
    border-radius: 8px;
}

.light .auth-container {
    background-color: rgba(0, 0, 0, 0.02);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.dark .auth-container {
    background-color: rgba(255, 255, 255, 0.02);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.form-group {
    margin-bottom: 20px;
    text-align: left;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
}

.form-group.checkbox {
    display: flex;
    align-items: center;
}

.form-group.checkbox label {
    margin-bottom: 0;
    margin-left: 10px;
}

.form-control {
    width: 100%;
    padding: 10px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 4px;
    font-size: 16px;
    transition: border-color 0.3s ease;
}

.dark .form-control {
    background-color: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.1);
    color: #f5f5f5;
}

.form-control:focus {
    outline: none;
    border-color: #5865F2;
}

.error {
    color: #e74c3c;
    font-size: 14px;
    margin-top: 5px;
    display: block;
}

.auth-links {
    margin-top: 20px;
    text-align: center;
}

/* Settings Page Styles */
.settings-section {
    padding: 60px 0;
    text-align: center;
}

.settings-section h1 {
    font-size: 2.2rem;
    margin-bottom: 40px;
}

.settings-container {
    max-width: 500px;
    margin: 0 auto;
    padding: 30px;
    border-radius: 8px;
}

.light .settings-container {
    background-color: rgba(0, 0, 0, 0.02);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.dark .settings-container {
    background-color: rgba(255, 255, 255, 0.02);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

/* Checkout Success/Cancel Pages */
.checkout-success, .checkout-cancel {
    padding: 60px 0;
    text-align: center;
}

.success-container, .cancel-container {
    max-width: 700px;
    margin: 0 auto;
    padding: 40px;
    border-radius: 10px;
}

.light .success-container, .light .cancel-container {
    background-color: rgba(0, 0, 0, 0.02);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.dark .success-container, .dark .cancel-container {
    background-color: rgba(255, 255, 255, 0.02);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.checkout-success h1, .checkout-cancel h1 {
    font-size: 2.2rem;
    margin-bottom: 20px;
}

.checkout-success p, .checkout-cancel p {
    margin-bottom: 20px;
    font-size: 1.1rem;
}

.next-steps {
    margin: 40px 0;
    padding: 20px;
    border-radius: 8px;
    text-align: left;
}

.light .next-steps {
    background-color: rgba(0, 0, 0, 0.03);
}

.dark .next-steps {
    background-color: rgba(255, 255, 255, 0.03);
}

.next-steps h2 {
    margin-bottom: 15px;
}

/* Buttons */
.cta-button {
    display: inline-block;
    padding: 12px 25px;
    font-weight: bold;
    border-radius: 5px;
    cursor: pointer;
    border: none;
    transition: all 0.3s ease;
}

.light .cta-button {
    background-color: #333;
    color: white !important;
}

.dark .cta-button {
    background-color: #f5f5f5;
    color: #333 !important;
}

.cta-button:hover {
    transform: translateY(-2px);
    opacity: 0.9;
}

.cta-button.secondary {
    background-color: transparent;
    border: 2px solid;
}

.light .cta-button.secondary {
    border-color: #333;
    color: #333 !important;
}

.dark .cta-button.secondary {
    border-color: #f5f5f5;
    color: #f5f5f5 !important;
}

/* Footer */
footer {
    padding: 50px 0 20px;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.light footer {
    background-color: rgba(0, 0, 0, 0.02);
    border-top-color: rgba(0, 0, 0, 0.1);
}

.dark footer {
    background-color: rgba(0, 0, 0, 0.1);
    border-top-color: rgba(255, 255, 255, 0.1);
}

.footer-content {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin-bottom: 30px;
}

.footer-logo img {
    height: 40px;
    margin-bottom: 15px;
}

.footer-links ul {
    list-style: none;
}

.footer-links li {
    margin-bottom: 10px;
}

.footer-contact {
    text-align: right;
}

.footer-contact p {
    margin-bottom: 5px;
    font-weight: bold;
}

.footer-bottom {
    text-align: center;
    padding-top: 20px;
    border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.dark .footer-bottom {
    border-top-color: rgba(255, 255, 255, 0.05);
}

/* Responsive Design */
@media (max-width: 768px) {
    header .container {
        flex-direction: column;
    }
    
    .logo {
        margin-bottom: 15px;
    }
    
    nav ul {
        margin-bottom: 15px;
    }
    
    .hero-content h1 {
        font-size: 2rem;
    }
    
    .footer-content {
        flex-direction: column;
        text-align: center;
    }
    
    .footer-logo, .footer-links, .footer-contact {
        margin-bottom: 20px;
        text-align: center;
    }
    
    .pricing-card.featured {
        transform: none;
    }
}

@media (max-width: 480px) {
    nav ul {
        flex-wrap: wrap;
        justify-content: center;
    }
    
    nav ul li {
        margin: 5px;
    }
    
    .hero-content h1 {
        font-size: 1.8rem;
    }
    
    .theme-toggle, .language-toggle {
        justify-content: center;
        margin-top: 10px;
    }
}
"""

# ==================
# JAVASCRIPT
# ==================

js_main = """
// Initialize Particles.js
document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('particles-js');
    
    // Only create particles in canvases that exist
    if (canvas) {
        const particleOptions = {
            particleColor: document.body.classList.contains('dark') ? '#ffffff' : '#000000',
            particleRadius: 2,
            speed: 0.5,
            connectParticles: false,
            maxParticles: 100
        };
        
        new ParticlesJS(canvas, particleOptions);
        
        // Enable particle connections on mouse hover
        canvas.addEventListener('mousemove', function() {
            particleOptions.connectParticles = true;
            canvas.particlesInstance.connectParticles = true;
        });
        
        // Disable particle connections when mouse stops
        let timeout;
        canvas.addEventListener('mousemove', function() {
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                particleOptions.connectParticles = false;
                canvas.particlesInstance.connectParticles = false;
            }, 3000);
        });
    }
    
    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Close all FAQs
            faqItems.forEach(faq => {
                faq.classList.remove('active');
            });
            
            // If the clicked one wasn't active, make it active
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
    
    // Countdown Timer
    const countdownEl = document.getElementById('countdown');
    
    if (countdownEl) {
        // Start with 48 hours (48 * 60 * 60 * 1000 ms)
        let timeLeft = 48 * 60 * 60;
        
        // Get saved countdown from localStorage if it exists
        const savedTime = localStorage.getItem('specialOfferCountdown');
        const startTime = localStorage.getItem('countdownStartTime');
        
        if (savedTime && startTime) {
            // Calculate elapsed time since the countdown started
            const elapsedSeconds = Math.floor((Date.now() - parseInt(startTime)) / 1000);
            timeLeft = parseInt(savedTime) - elapsedSeconds;
            
            // Reset if the countdown is finished or negative
            if (timeLeft <= 0) {
                timeLeft = 48 * 60 * 60;
                localStorage.setItem('countdownStartTime', Date.now().toString());
            }
        } else {
            // Initialize countdown if not saved
            localStorage.setItem('specialOfferCountdown', timeLeft.toString());
            localStorage.setItem('countdownStartTime', Date.now().toString());
        }
        
        // Update countdown every second
        function updateCountdown() {
            const hours = Math.floor(timeLeft / 3600);
            const minutes = Math.floor((timeLeft % 3600) / 60);
            const seconds = timeLeft % 60;
            
            countdownEl.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
            if (timeLeft <= 0) {
                timeLeft = 48 * 60 * 60;
                localStorage.setItem('countdownStartTime', Date.now().toString());
            } else {
                timeLeft--;
                localStorage.setItem('specialOfferCountdown', timeLeft.toString());
            }
        }
        
        // Initialize and start countdown
        updateCountdown();
        setInterval(updateCountdown, 1000);
    }
});
"""

js_particles = """
!function(e,t){"object"==typeof exports&&"undefined"!=typeof module?module.exports=t():"function"==typeof define&&define.amd?define(t):e.ParticlesJS=t()}(this,function(){"use strict";function e(e,t){return t={exports:{}},e(t,t.exports),t.exports}var t=e(function(e,t){Object.defineProperty(t,"__esModule",{value:!0});var n=function(){function e(e,t){for(var n=0;n<t.length;n++){var i=t[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}return function(t,n,i){return n&&e(t.prototype,n),i&&e(t,i),t}}();var i=function(){function e(t,n){var i=this;!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),this.canvas=t,this.ctx=t.getContext("2d"),this.particlesArray=[],this.canvasWidth=t.width,this.canvasHeight=t.height,this.options=n,this.connectParticles=n.connectParticles||!1;var a=this.options.maxParticles||100;for(var r=0;r<a;r++)this.particlesArray.push(new Particle(this.canvas,this.options));this.animate=this.animate.bind(this),this.animate(),window.addEventListener("resize",function(){i.resize()},!1)}return n(e,[{key:"animate",value:function(){var e=this;this.ctx.clearRect(0,0,this.canvasWidth,this.canvasHeight),this.particlesArray.forEach(function(t,n){t.draw(),t.update(),e.connectParticles&&e.connect(t,e.particlesArray.slice(n))}),requestAnimationFrame(this.animate)}},{key:"connect",value:function(e,t){var n=this,i=this.options.connectDistance||100,a=this.options.connectLineWidth||1,r=this.options.connectLineColor||"#ffffff";t.forEach(function(t){var o=Math.sqrt(Math.pow(e.x-t.x,2)+Math.pow(e.y-t.y,2));if(o<i){var s=1-o/i;n.ctx.beginPath(),n.ctx.strokeStyle=r,n.ctx.lineWidth=s*a,n.ctx.moveTo(e.x,e.y),n.ctx.lineTo(t.x,t.y),n.ctx.stroke()}})}},{key:"resize",value:function(){var e=this;this.canvas.width=window.innerWidth,this.canvas.height=window.innerHeight,this.canvasWidth=this.canvas.width,this.canvasHeight=this.canvas.height,this.particlesArray.forEach(function(t){t.containerWidth=e.canvasWidth,t.containerHeight=e.canvasHeight})}}]),e}();var Particle=function(){function e(t,n){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),this.canvas=t,this.options=n,this.x=Math.random()*t.width,this.y=Math.random()*t.height,this.velocity={x:(Math.random()-.5)*n.speed||1,y:(Math.random()-.5)*n.speed||1},this.radius=n.particleRadius||3,this.color=n.particleColor||"#ffffff",this.containerWidth=t.width,this.containerHeight=t.height}return n(e,[{key:"update",value:function(){this.x+this.velocity.x+this.radius>this.containerWidth||this.x+this.velocity.x-this.radius<0?this.velocity.x=-this.velocity.x:this.y+this.velocity.y+this.radius>this.containerHeight||this.y+this.velocity.y-this.radius<0?this.velocity.y=-this.velocity.y:(this.x+=this.velocity.x,this.y+=this.velocity.y)}},{key:"draw",value:function(){var e=this.canvas.getContext("2d");e.beginPath(),e.arc(this.x,this.y,this.radius,0,2*Math.PI),e.fillStyle=this.color,e.fill()}}]),e}();t.default=i});return t.default});

// Add the ParticlesJS to the canvas
function initParticles(containerId, options) {
    const canvas = document.getElementById(containerId);
    if (canvas) {
        return new ParticlesJS(canvas, options);
    }
    return null;
}
"""

# Base64 encoded logo and favicon data
# These would normally be loaded from files but for our all-in-one approach,
# we embed them as base64 strings
logo_data = "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"
favicon_data = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAr0lEQVQ4jWNgGAXDADCCCJM93zkMzjDMBjE+Nz7I8N79PYazvmf9Z2BgYPhf9/8/AwMDAwP/dH4GBgYGBqZtTOeZGZlrQZrm3Z/HsOD+gv/H/x9nYGBgYJA7J8ewpGAJw7r6dQx8p/kYlhQsYWBgYGCQ2yjHwLSSiYEBiB/8f/D/wf8H/5//f/5f9pzsfyY2pu1MjEwM7rLubxnYGNg4GTkZTra5MzAwMDAwsDOwj4JRMJQAAKz6Li8v/sAKAAAAAElFTkSuQmCC"

# ==================
# MAIN EXECUTION
# ==================

if __name__ == "__main__":
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
    # Start the Flask application
    app.run(host="0.0.0.0", port=5000, debug=True)