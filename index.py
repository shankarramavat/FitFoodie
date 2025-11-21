import sys
import os

# Add trio to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'trio'))

# Set environment variables if not already set (for local .env loading)
os.environ.setdefault('FLASK_SECRET_KEY', 'default_secret_key')
os.environ.setdefault('MYSQL_HOST', 'localhost')
os.environ.setdefault('MYSQL_USER', 'root')
os.environ.setdefault('MYSQL_PASSWORD', 'root')
os.environ.setdefault('MYSQL_DB', 'geeklogin')

from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import re
import json
import base64
from io import BytesIO

app = Flask(__name__, 
            template_folder='trio/templates',
            static_folder='trio/static')

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

# MySQL configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'geeklogin')

# Lazy import helpers
_pymysql = None
_food_identifier = None
_nutrients = None
_Image = None
_secure_filename = None

def get_pymysql():
    global _pymysql
    if _pymysql is None:
        import pymysql
        _pymysql = pymysql
    return _pymysql

def get_food_identifier():
    global _food_identifier
    if _food_identifier is None:
        from ml_model import food_identifier
        _food_identifier = food_identifier
    return _food_identifier

def get_nutrients():
    global _nutrients
    if _nutrients is None:
        from food import nutrients
        _nutrients = nutrients
    return _nutrients

def get_image():
    global _Image
    if _Image is None:
        from PIL import Image
        _Image = Image
    return _Image

def get_secure_filename():
    global _secure_filename
    if _secure_filename is None:
        from werkzeug.utils import secure_filename
        _secure_filename = secure_filename
    return _secure_filename

# MySQL Connection Manager
class MySQL:
    def __init__(self, app=None):
        self.app = app
        self._connection_available = None
        if app:
            self.init_app(app)
            
    def init_app(self, app):
        self.app = app
        @app.teardown_appcontext
        def close_db(error):
            db = getattr(g, '_database', None)
            if db is not None:
                db.close()

    @property
    def connection(self):
        db = getattr(g, '_database', None)
        if db is None:
            try:
                pymysql = get_pymysql()
                db = g._database = pymysql.connect(
                    host=self.app.config['MYSQL_HOST'],
                    user=self.app.config['MYSQL_USER'],
                    password=self.app.config['MYSQL_PASSWORD'],
                    db=self.app.config['MYSQL_DB']
                )
                self._connection_available = True
            except Exception as e:
                self._connection_available = False
                raise Exception(f"Database connection failed. Please set up a cloud database. Error: {str(e)}")
        return db
    
    def is_available(self):
        if self._connection_available is None:
            try:
                _ = self.connection
                return True
            except:
                return False
        return self._connection_available

mysql = MySQL(app)

# Routes
@app.route('/')
def home():
    login = False
    if 'loggedin' in session:
        login = True
        return render_template('home.html', username=session.get('username'), login=login)
    return render_template('home.html', login=login)

@app.route('/status')
def status():
    db_status = "❌ Not Connected"
    db_error = None
    try:
        _ = mysql.connection
        db_status = "✅ Connected"
    except Exception as e:
        db_error = str(e)
    
    return f"""
    <html>
    <head>
        <title>FitFoodie - Status</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .status {{ padding: 20px; border-radius: 5px; margin: 10px 0; }}
            .success {{ background: #d4edda; color: #155724; }}
            .error {{ background: #f8d7da; color: #721c24; }}
        </style>
    </head>
    <body>
        <h1>🏥 FitFoodie Status</h1>
        <div class="status {'success' if 'Connected' in db_status else 'error'}">
            <h2>Database: {db_status}</h2>
            {f'<p>{db_error}</p>' if db_error else ''}
        </div>
        <hr>
        <p><strong>Environment Variables:</strong></p>
        <ul>
            <li>MYSQL_HOST: {app.config['MYSQL_HOST']}</li>
            <li>MYSQL_USER: {app.config['MYSQL_USER']}</li>
            <li>MYSQL_DB: {app.config['MYSQL_DB']}</li>
            <li>FLASK_SECRET_KEY: {'Set' if app.secret_key != 'default_secret_key' else 'Using default'}</li>
        </ul>
        <p><a href="/">← Go Home</a></p>
    </body>
    </html>
    """


@app.route('/fitFoodie/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        try:
            email = request.form['email']
            password = request.form['password']
            pymysql = get_pymysql()
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                return redirect(url_for('home'))
            else:
                msg = 'Incorrect username / password!'
        except Exception as e:
            msg = f'Database error: {str(e)}'
    return render_template('login.html', msg=msg)

@app.route('/fitFoodie/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/fitFoodie/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        try:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            pymysql = get_pymysql()
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
                mysql.connection.commit()
                msg = 'You have successfully registered!'
                return redirect(url_for('login'))
        except Exception as e:
            msg = f'Database error: {str(e)}'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/fitFoodie/profile')
def profile():
    login = False
    if 'loggedin' in session:
        try:
            login = True
            pymysql = get_pymysql()
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
            account = cursor.fetchone()
            return render_template('profile.html', account=account, login=login)
        except Exception as e:
            return f"Database error: {str(e)}", 500
    return redirect(url_for('login'))

# Error handler
@app.errorhandler(500)
def internal_error(error):
    return f"""
    <html>
    <head><title>Error</title></head>
    <body>
        <h1>Internal Server Error</h1>
        <p>{str(error)}</p>
        <p><a href="/">Go Home</a></p>
    </body>
    </html>
    """, 500

# Vercel will use this app instance
