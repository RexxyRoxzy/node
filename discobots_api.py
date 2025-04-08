"""
DiscoBots.fr - API Backend
This file contains the Flask API backend for the DiscoBots.fr website.
It provides API endpoints for authentication, user management, and payment processing.

Requirements:
Flask==2.3.3
flask-login==0.6.2
flask-sqlalchemy==3.1.1 
flask-wtf==1.1.1
flask-cors==4.0.0
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
   - FRONTEND_URL: URL of your frontend (for CORS)
3. Run: python discobots_api.py
"""

import os
import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, g, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import jwt
from functools import wraps

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

# Configure CORS to allow requests from your frontend
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")
CORS(app, origins=[FRONTEND_URL], supports_credentials=True)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db.init_app(app)

# Configure Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# JWT settings
JWT_SECRET = os.environ.get("JWT_SECRET", app.secret_key)
JWT_EXPIRATION = 24 * 60 * 60  # 24 hours in seconds

# ==================
# DATABASE MODELS
# ==================

class User(db.Model):
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
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'theme': self.theme,
            'language': self.language
        }

# ==================
# JWT FUNCTIONS
# ==================

def generate_token(user_id):
    """Generate a JWT token for the user"""
    payload = {
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def token_required(f):
    """Decorator to protect API routes with JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
            
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user = User.query.get(payload['sub'])
            if not user:
                return jsonify({'message': 'User not found'}), 401
            g.user = user
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
            
        return f(*args, **kwargs)
    return decorated

# ==================
# API ROUTES
# ==================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'message': 'Missing required fields'}), 400
        
    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already in use'}), 400
        
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already in use'}), 400
    
    # Create new user
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    # Set optional fields if provided
    if 'theme' in data:
        user.theme = data['theme']
    if 'language' in data:
        user.language = data['language']
        
    db.session.add(user)
    db.session.commit()
    
    # Generate JWT token
    token = generate_token(user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': user.to_dict()
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ('username', 'password')):
        return jsonify({'message': 'Missing username or password'}), 400
        
    # Find user
    user = User.query.filter_by(username=data['username']).first()
    
    # Check password
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    # Generate JWT token
    token = generate_token(user.id)
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    }), 200

@app.route('/api/user', methods=['GET'])
@token_required
def get_user():
    """Get current user's information"""
    return jsonify({
        'user': g.user.to_dict()
    }), 200

@app.route('/api/settings', methods=['PUT'])
@token_required
def update_settings():
    """Update user settings"""
    data = request.get_json()
    
    if 'theme' in data:
        g.user.theme = data['theme']
    
    if 'language' in data:
        g.user.language = data['language']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Settings updated successfully',
        'user': g.user.to_dict()
    }), 200

@app.route('/api/create-checkout-session', methods=['POST'])
@token_required
def create_checkout_session():
    """Create a Stripe checkout session"""
    data = request.get_json()
    
    try:
        # The product ID for DiscoBots Standard plan
        product_id = "prod_S5lpY8QkDBwJhx"
        
        # Apply discount voucher if provided
        discount_code = None
        if 'voucher' in data and data['voucher'] == 'Uflvb62d':
            discount_code = 'Uflvb62d'
        
        # Get the success and cancel URLs from the frontend
        success_url = data.get('success_url', f"{FRONTEND_URL}/checkout-success")
        cancel_url = data.get('cancel_url', f"{FRONTEND_URL}/checkout-cancel")
        
        # Create line items
        line_items = [{
            'price': product_id,
            'quantity': 1,
        }]
        
        # Create checkout session
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            discounts=[{'coupon': discount_code}] if discount_code else [],
            client_reference_id=str(g.user.id),  # For identifying the user later
        )
        
        return jsonify({
            'url': checkout_session.url
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================
# MAIN EXECUTION
# ==================

if __name__ == "__main__":
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
    # Start the Flask application
    app.run(host="0.0.0.0", port=5000, debug=True)