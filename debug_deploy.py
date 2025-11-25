from flask import Flask
import pymysql
import os
import traceback

app = Flask(__name__)

# Hardcoded credentials for debugging
MYSQL_HOST = 'interchange.proxy.rlwy.net'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'EmoLxiyvQALpwpAwrniXpYeJhpIhjavo'
MYSQL_DB = 'railway'
MYSQL_PORT = 48465

@app.route('/')
def home():
    return "<h1>Debug Mode</h1><p>Go to <a href='/test-db'>/test-db</a> to check database connection.</p>"

@app.route('/test-db')
def test_db():
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DB,
            port=MYSQL_PORT,
            connect_timeout=5
        )
        connection.close()
        return "<h1>✅ Database Connection Successful!</h1><p>The credentials are correct and the app can connect.</p>"
    except Exception as e:
        return f"<h1>❌ Connection Failed</h1><pre>{traceback.format_exc()}</pre>"

# Vercel handler
handler = app
