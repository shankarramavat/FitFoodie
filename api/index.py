import os
import sys

# Add the parent directory to sys.path so we can import from the root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from index import app

# Vercel expects a 'handler' function, but for Flask, 
# simply importing 'app' is often enough if using 'vercel.json' correctly.
# However, explicitly defining handler can help.
# But with @vercel/python, 'app' is usually detected.
# We will just expose 'app' as the WSGI application.
