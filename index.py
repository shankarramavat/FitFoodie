import sys
import os
from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect, url_for, session, g
import re

# Add the trio package to the import path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "trio"))

# Load local .env defaults (only used when running locally)
os.environ.setdefault('FLASK_SECRET_KEY', 'default_secret_key')
os.environ.setdefault('MYSQL_HOST', 'localhost')
os.environ.setdefault('MYSQL_USER', 'root')
os.environ.setdefault('MYSQL_PASSWORD', 'root')
os.environ.setdefault('MYSQL_DB', 'geeklogin')

app = Flask(__name__, template_folder='trio/templates', static_folder='trio/static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

# -------------------------------------------------
# Database configuration – Hardcoded for Vercel Fix
# -------------------------------------------------
# Credentials extracted from: mysql://root:EmoLxiyvQALpwpAwrniXpYeJhpIhjavo@interchange.proxy.rlwy.net:48465/railway
app.config['MYSQL_HOST'] = 'interchange.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'EmoLxiyvQALpwpAwrniXpYeJhpIhjavo'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_PORT'] = 48465

# Fallback logic removed since we are hardcoding for immediate fix


# -------------------------------------------------
# Lazy import helper for pymysql
# -------------------------------------------------
_pymysql = None

def get_pymysql():
    """Import pymysql only when needed."""
    global _pymysql
    if _pymysql is None:
        import pymysql
        _pymysql = pymysql
    return _pymysql

# -------------------------------------------------
# MySQL connection manager
# -------------------------------------------------
class MySQL:
    def __init__(self, app=None):
        self._connection_available = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Register teardown hook."""
        @app.teardown_appcontext
        def close_db(error):
            db = getattr(g, '_database', None)
            if db is not None:
                db.close()

    @property
    def connection(self):
        """Create a connection on first use, with clear error messages."""
        db = getattr(g, '_database', None)
        if db is None:
            host = app.config.get('MYSQL_HOST')
            user = app.config.get('MYSQL_USER')
            password = app.config.get('MYSQL_PASSWORD')
            db_name = app.config.get('MYSQL_DB')
            port = int(app.config.get('MYSQL_PORT', 3306))
            missing = [name for name, val in [
                ('MYSQL_HOST', host),
                ('MYSQL_USER', user),
                ('MYSQL_PASSWORD', password),
                ('MYSQL_DB', db_name)
            ] if not val]
            if missing:
                raise Exception(f"Missing required DB env vars: {', '.join(missing)}")
            pymysql = get_pymysql()
            db = g._database = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db_name,
                port=port,
                connect_timeout=5,
            )
            self._connection_available = True
        return db

    def is_available(self):
        """Quick health-check used by the /status route."""
        if self._connection_available is None:
            try:
                _ = self.connection
                return True
            except Exception:
                return False
        return self._connection_available

# Initialise the helper
mysql = MySQL(app)

# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route('/')
def home():
    login = 'loggedin' in session
    return render_template('home.html', username=session.get('username'), login=login)

@app.route('/status')
def status():
    db_status = '❌ Not Connected'
    db_error = None
    try:
        _ = mysql.connection
        db_status = '✅ Connected'
    except Exception as e:
        db_error = str(e)
    return f"""<!doctype html>
<html>
<head><title>FitFoodie – Status</title>
<style>
body {{font-family:Arial,sans-serif;margin:40px;}}
.status {{padding:20px;border-radius:5px;margin:10px 0;}}
.success {{background:#d4edda;color:#155724;}}
.error {{background:#f8d7da;color:#721c24;}}
</style>
</head>
<body>
<h1>🏥 FitFoodie Status</h1>
<div class="status {'success' if '✅' in db_status else 'error'}">
<h2>Database: {db_status}</h2>
{f'<p>{db_error}</p>' if db_error else ''}
</div>
<hr>
<p><strong>Environment Variables:</strong></p>
<ul>
<li>MYSQL_HOST: {app.config.get('MYSQL_HOST')}</li>
<li>MYSQL_USER: {app.config.get('MYSQL_USER')}</li>
<li>MYSQL_DB: {app.config.get('MYSQL_DB')}</li>
<li>FLASK_SECRET_KEY: {'Set' if app.secret_key != 'default_secret_key' else 'Using default'}</li>
</ul>
<p><a href="/">← Go Home</a></p>
</body>
</html>"""

@app.route('/fitFoodie/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        try:
            email = request.form['email']
            password = request.form['password']
            pymysql = get_pymysql()
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE email=%s AND password=%s', (email, password))
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
            cursor.execute('SELECT * FROM accounts WHERE username=%s', (username,))
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
                return redirect(url_for('login'))
        except Exception as e:
            msg = f'Database error: {str(e)}'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/fitFoodie/profile')
def profile():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    try:
        pymysql = get_pymysql()
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id=%s', (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account, login=True)
    except Exception as e:
        return f'Database error: {str(e)}', 500

# Debug route – shows env vars (remove after you confirm everything works)
@app.route('/debug-env')
def debug_env():
    env = {
        'MYSQL_HOST': app.config.get('MYSQL_HOST'),
        'MYSQL_USER': app.config.get('MYSQL_USER'),
        'MYSQL_DB': app.config.get('MYSQL_DB'),
        'MYSQL_PORT': app.config.get('MYSQL_PORT'),
    }
    return env

# New route to dump all environment variables (for debugging only)
@app.route('/env-all')
def env_all():
    # Return a JSON representation of selected environment variables
    selected = {k: v for k, v in os.environ.items() if k.startswith('MYSQL') or k in ['FLASK_SECRET_KEY', 'CLARIFAI_API_KEY', 'WOLFRAM_APP_ID']}
    return selected

# Generic error handler
@app.errorhandler(500)
def internal_error(error):
    return f"""<!doctype html>
<html>
<head><title>Error</title></head>
<body>
<h1>Internal Server Error</h1>
<p>{str(error)}</p>
<p><a href='/'>Go Home</a></p>
</body>
</html>""", 500

# Vercel requires a 'handler' variable for the entry point
handler = app
