import sys
import os
import traceback

# Add the trio directory to the path so we can import app.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'trio'))

try:
    # Import the main Flask app from trio/app.py
    from app import app as application

    # -------------------------------------------------
    # INJECT HARDCODED DATABASE CREDENTIALS
    # -------------------------------------------------
    # This forces the app to use the correct Railway DB, ignoring missing env vars
    application.config['MYSQL_HOST'] = 'interchange.proxy.rlwy.net'
    application.config['MYSQL_USER'] = 'root'
    application.config['MYSQL_PASSWORD'] = 'EmoLxiyvQALpwpAwrniXpYeJhpIhjavo'
    application.config['MYSQL_DB'] = 'railway'
    application.config['MYSQL_PORT'] = 48465
    
    # Ensure secret key is set
    application.secret_key = os.getenv('FLASK_SECRET_KEY', 'fixed_secret_key_for_vercel')

    # Vercel expects 'app' or 'handler'
    app = application
    handler = application

except Exception as e:
    # Catch any import errors (like missing dependencies) and show them
    error_details = traceback.format_exc()
    from flask import Flask
    app = Flask(__name__)
    @app.route('/')
    @app.route('/<path:path>')
    def catch_all(path=''):
        return f"<h1>Critical Startup Error</h1><pre>{error_details}</pre>", 500
    handler = app
