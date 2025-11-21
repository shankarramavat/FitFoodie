import sys
import os

# Add trio to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'trio'))

# Try to import the full app
try:
    from app import app
    print("✅ Successfully imported app from trio/app.py")
except ImportError as e:
    print(f"❌ Import Error: {e}")
    # Create a fallback app that shows the error
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    @app.route('/<path:path>')
    def error_handler(path=''):
        import traceback
        error_details = traceback.format_exc()
        return f"""
        <html>
        <head>
            <title>Import Error - FitFoodie</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                pre {{ background: #f4f4f4; padding: 20px; overflow-x: auto; }}
                .error {{ color: #d32f2f; }}
            </style>
        </head>
        <body>
            <h1 class="error">❌ Application Import Failed</h1>
            <h2>Error Details:</h2>
            <pre>{str(e)}</pre>
            <h2>Full Traceback:</h2>
            <pre>{error_details}</pre>
            <hr>
            <h3>Debugging Info:</h3>
            <p><strong>Python Version:</strong> {sys.version}</p>
            <p><strong>Working Directory:</strong> {os.getcwd()}</p>
            <p><strong>Python Path:</strong></p>
            <pre>{chr(10).join(sys.path)}</pre>
        </body>
        </html>
        """, 500
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    @app.route('/<path:path>')
    def error_handler(path=''):
        import traceback
        error_details = traceback.format_exc()
        return f"""
        <html>
        <head>
            <title>Unexpected Error - FitFoodie</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                pre {{ background: #f4f4f4; padding: 20px; overflow-x: auto; }}
                .error {{ color: #d32f2f; }}
            </style>
        </head>
        <body>
            <h1 class="error">❌ Unexpected Error During Import</h1>
            <h2>Error Details:</h2>
            <pre>{str(e)}</pre>
            <h2>Full Traceback:</h2>
            <pre>{error_details}</pre>
        </body>
        </html>
        """, 500

# Vercel will use this app instance
