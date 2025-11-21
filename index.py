import sys
import os

# Add trio to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'trio'))

try:
    from app import app
except Exception as e:
    # If import fails, create a simple Flask app that shows the error
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    @app.route('/<path:path>')
    def error_page(path=''):
        return f"""
        <html>
        <head><title>Import Error</title></head>
        <body>
            <h1>Application Import Error</h1>
            <p>Failed to import the main application.</p>
            <pre>{str(e)}</pre>
            <hr>
            <p>Python version: {sys.version}</p>
            <p>Python path: {sys.path}</p>
        </body>
        </html>
        """, 500

# This is what Vercel will use
