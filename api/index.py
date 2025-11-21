import sys
import os

# Add the trio directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'trio'))

# Import the Flask app
from app import app

# This is the handler that Vercel will use
def handler(request, response):
    return app(request, response)
