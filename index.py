import sys
import os

# Add the trio directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'trio'))

# Create a simple Flask app to test
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>FitFoodie - Deployment Test</h1>
    <p>If you see this, the basic Flask app is working!</p>
    <p>Now testing imports...</p>
    """

@app.route('/test-imports')
def test_imports():
    results = []
    
    # Test each import individually
    try:
        import pymysql
        results.append("✓ pymysql imported successfully")
    except Exception as e:
        results.append(f"✗ pymysql failed: {str(e)}")
    
    try:
        from PIL import Image
        results.append("✓ Pillow imported successfully")
    except Exception as e:
        results.append(f"✗ Pillow failed: {str(e)}")
    
    try:
        import requests
        results.append("✓ requests imported successfully")
    except Exception as e:
        results.append(f"✗ requests failed: {str(e)}")
    
    try:
        import wolframalpha
        results.append("✓ wolframalpha imported successfully")
    except Exception as e:
        results.append(f"✗ wolframalpha failed: {str(e)}")
    
    try:
        from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
        results.append("✓ clarifai_grpc imported successfully")
    except Exception as e:
        results.append(f"✗ clarifai_grpc failed: {str(e)}")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'trio'))
        from app import app as main_app
        results.append("✓ Main app imported successfully")
    except Exception as e:
        results.append(f"✗ Main app import failed: {str(e)}")
    
    html = "<h1>Import Test Results</h1><ul>"
    for result in results:
        html += f"<li>{result}</li>"
    html += "</ul>"
    
    return html

# Vercel needs this
handler = app
