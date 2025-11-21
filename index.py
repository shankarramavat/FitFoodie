from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head><title>FitFoodie - Test</title></head>
    <body>
        <h1>✅ Flask is Working on Vercel!</h1>
        <p>If you see this, the basic Flask deployment is successful.</p>
        <p>Next step: Add the full application code.</p>
    </body>
    </html>
    """

@app.route('/<path:path>')
def catch_all(path):
    return f"""
    <html>
    <head><title>Route Test</title></head>
    <body>
        <h1>Route: /{path}</h1>
        <p>Flask routing is working!</p>
        <a href="/">Go Home</a>
    </body>
    </html>
    """

# Vercel will use this app instance
