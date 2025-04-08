import os
from flask import Flask, render_template

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "development-secret-key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/discord')
def discord():
    return render_template('discord.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')
