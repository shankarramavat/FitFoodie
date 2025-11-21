import sys
import os

# Add the trio directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'trio'))

# Import the Flask app
from app import app

# Vercel expects the app instance directly
# The app variable is automatically used as the WSGI application

