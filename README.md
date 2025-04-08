# DiscoBots.fr

A website for a Discord bot service featuring user authentication, theme switching, and language selection.

## Project Structure

This project is split into two parts:

1. **Frontend**: Static HTML/CSS/JS that can be deployed on Netlify
2. **Backend API**: Flask application that provides API endpoints for the frontend

## Frontend Deployment (Netlify)

The frontend is a static site that can be deployed directly to Netlify.

### Steps to Deploy Frontend to Netlify:

1. **Create a Netlify account** if you don't have one already
2. **Connect your GitHub repository** to Netlify
3. **Configure build settings**:
   - Base directory: `frontend`
   - Publish directory: `/`
   - Build command: (leave empty for this static site)
4. **Set environment variables**:
   - `API_URL`: The URL of your backend API (e.g., https://your-api-server.herokuapp.com)
5. **Deploy**

Alternatively, you can simply drag and drop the `frontend` directory to Netlify's deploy area.

## Backend API Deployment

The backend API is a Flask application that needs to be deployed to a Python-friendly hosting platform.

### Option 1: Deploy to Heroku

1. **Create a Heroku account** if you don't have one already
2. **Install the Heroku CLI** and log in
3. **Create a Heroku app**:
   ```
   heroku create discobots-api
   ```
4. **Add PostgreSQL addon**:
   ```
   heroku addons:create heroku-postgresql:hobby-dev
   ```
5. **Set environment variables**:
   ```
   heroku config:set FLASK_APP=discobots_api.py
   heroku config:set SECRET_KEY=your_secret_key
   heroku config:set STRIPE_SECRET_KEY=your_stripe_secret_key
   heroku config:set FRONTEND_URL=https://your-netlify-site.netlify.app
   ```
6. **Create a Procfile** in the root directory:
   ```
   web: gunicorn discobots_api:app
   ```
7. **Deploy to Heroku**:
   ```
   git push heroku main
   ```

### Option 2: Deploy to PythonAnywhere

1. **Create a PythonAnywhere account**
2. **Upload the backend files**
3. **Create a virtual environment and install dependencies**:
   ```
   pip install -r api_requirements.txt
   ```
4. **Configure a new web app**:
   - Framework: Flask
   - Python version: 3.8 or newer
   - Path to WSGI: `/path/to/discobots_api.py`
5. **Set environment variables** in the WSGI configuration file
6. **Add a custom domain** if desired

## Environment Variables

### Backend API Environment Variables:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY` (or `SESSION_SECRET`): Random string for Flask session encryption
- `STRIPE_SECRET_KEY`: Your Stripe secret key
- `FRONTEND_URL`: URL of your frontend (for CORS)
- `JWT_SECRET`: Secret key for JWT token signing (defaults to SESSION_SECRET if not set)

### Frontend Environment Variables:

- `API_URL`: URL of your backend API

## API Endpoints

The backend API provides these endpoints:

- `POST /api/register`: Register a new user
- `POST /api/login`: Log in an existing user
- `GET /api/user`: Get current user information
- `PUT /api/settings`: Update user settings
- `POST /api/create-checkout-session`: Create a Stripe checkout session

## Development

To run the frontend locally, simply open the HTML files in a browser.

To run the backend API locally:

1. Install dependencies:
   ```
   pip install -r api_requirements.txt
   ```
2. Set environment variables:
   ```
   export DATABASE_URL=postgresql://localhost/discobots
   export SECRET_KEY=dev_secret_key
   export STRIPE_SECRET_KEY=your_test_stripe_key
   export FRONTEND_URL=http://localhost:3000
   ```
3. Run the Flask development server:
   ```
   python discobots_api.py
   ```