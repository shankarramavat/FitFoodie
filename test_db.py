from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Deployment Test: V3</h1><p>If you see this, the new code is running.</p>"

@app.route('/status')
def status():
    return "<h1>Status: OK</h1>"
