import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask 
from flask import Blueprint,render_template,request,redirect,url_for,flash,session 
from flask import g
import pymysql

import re
import urllib.request 
import os 
from werkzeug.utils import secure_filename 
from PIL import Image 
from ml_model import food_identifier 
from food import nutrients
import datetime as DT
import datetime as DT
import json
import base64
from io import BytesIO


app = Flask(__name__)

class MySQL:
    def __init__(self, app=None):
        self.app = app
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
            db = g._database = pymysql.connect(
                host=self.app.config['MYSQL_HOST'],
                user=self.app.config['MYSQL_USER'],
                password=self.app.config['MYSQL_PASSWORD'],
                db=self.app.config['MYSQL_DB']
            )
        return db

mysql = MySQL(app)


app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'geeklogin')


# @app.route('/')
@app.route('/fitFoodie/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s AND password = % s', ( email, password, ))
        # cursor.execute('SELECT password FROM accounts WHERE email = % s', ( email, ))
        account = cursor.fetchone()
        print(account)
        if account:
            # Create session data, we can access this data in other route
            session['loggedin'] = True
            session['id'] = account['id']
            # session['email'] = account['email']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        # if account:
        #   print("Inside account")
        #   if account['password'] == password:
        #       msg = 'Logged in successfully !'
        #       return render_template('home.html', msg = msg,email=email,account=account)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/')
def home():
    # Check if user is loggedin
    login=False
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # User is not loggedin redirect to login page
        login=True
        return render_template('home.html', username=session['username'], login=login)
    return render_template('home.html', login=login)
    # return redirect(url_for('home'))

@app.route('/fitFoodie/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/fitFoodie/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            # print(msg)
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/fitFoodie/profile')
def profile():
    # Check if user is loggedin
    login=False
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        login=True
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account,login=login)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


UPLOAD_FOLDER = "static/uploads/"

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/fitFoodie/input',methods=['GET'])
def input():
    return render_template('input.html',login=True)


@app.route('/fitFoodie/output',methods=['POST'])
def upload_input():
    inp = request.form['inp']
    nutr=nutrients(inp)
    print(nutr)
    # print(nutr)
    nutrients_value=nutr[0]
    print(nutrients_value)
    # print(food_name)
    nutr=nutr[1]
    cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('INSERT INTO nutrients VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,DEFAULT)', (inp, session['id'],nutrients_value['fat'],nutrients_value['carbohydrates'],nutrients_value['cholesterol'],nutrients_value['protein'],nutrients_value['sodium'],))
    mysql.connection.commit()
    cursor.close()
    return render_template('result.html',nutr=nutr,login=True,inp=inp)



@app.route('/fitFoodie/upload',methods=['GET'])
def upload():
    return render_template('uploads.html',login=True)

@app.route('/fitFoodie/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Read file bytes into memory
        file_bytes = file.read()
        
        # Open image for resizing (optional, but good for display consistency)
        image = Image.open(BytesIO(file_bytes))
        
        # Resize for display/consistency if needed, but we process original bytes for ML usually
        # or we can process the resized bytes. Let's stick to original for ML accuracy 
        # unless it's too large.
        # For display, we'll use the resized version converted to base64
        
        resized_img = image.resize((400, 400))
        
        # Convert resized image to base64 for display
        buffered = BytesIO()
        resized_img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Use original bytes for ML (or resized if you prefer speed)
        # food_identifier now accepts bytes
        food_name = food_identifier(file_bytes)
        
        nutr=nutrients(food_name)
        print(food_name)
        # print(nutr)
        nutrients_value=nutr[0]
        print(nutrients_value)
        print(food_name)
        nutr=nutr[1]

        print(nutr)
        print(session['id'])
        print(nutrients_value['fat'])
        print(nutrients_value['carbohydrates'])
        print(nutrients_value['cholesterol'])
        print(nutrients_value['protein'])
        print(nutrients_value['sodium'])
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute('INSERT INTO nutrients VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,DEFAULT)', (food_name, session['id'],nutrients_value['fat'],nutrients_value['carbohydrates'],nutrients_value['cholesterol'],nutrients_value['protein'],nutrients_value['sodium'],))
        mysql.connection.commit()
        cursor.close()
        
        # Pass base64 string to template
        return render_template('uploads.html', filename=filename, image_data=img_str, food=food_name,nutr=nutr,login=True)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM nutrients WHERE u_id = %s', (session['id'],))
        data=cursor.fetchall()
        cursor.execute('SELECT sum(fat) FROM nutrients WHERE u_id = %s', (session['id'],))
        fat=cursor.fetchall()
        fat=fat[0]['sum(fat)']
        cursor.execute('SELECT sum(carbohydrates) FROM nutrients WHERE u_id = %s', (session['id'],))
        carbohydrates=cursor.fetchall()
        carbohydrates=carbohydrates[0]['sum(carbohydrates)']
        cursor.execute('SELECT sum(cholesterol) FROM nutrients WHERE u_id = %s', (session['id'],))
        cholesterol=cursor.fetchall()
        cholesterol=cholesterol[0]['sum(cholesterol)']
        cursor.execute('SELECT sum(protein) FROM nutrients WHERE u_id = %s', (session['id'],))
        protein=cursor.fetchall()
        protein=protein[0]['sum(protein)']
        cursor.execute('SELECT sum(sodium) FROM nutrients WHERE u_id = %s', (session['id'],))
        sodium=cursor.fetchall()
        sodium=sodium[0]['sum(sodium)']
        cursor.close()
        print(fat)
        # print("data",data[0]['fname'])
        # return redirect(url_for('getAllHistory',data=data))

        return render_template('dashboard.html',data=data,login=True,fat=fat,carbohydrates=carbohydrates,cholesterol=cholesterol,protein=protein,sodium=sodium)
    return render_template('dashboard.html')

    # return render_template('dashboard.html')

@app.route('/getAllHistory')
def getAllHistory():
    if 'loggedin' in session:
        print("hello")
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM nutrients WHERE u_id = %s', (session['id'],))
        data=cursor.fetchall()
        cursor.close()
        # print("data",data[0]['fname'])
        return render_template('dashboard.html',data=data)
    return render_template('dashboard.html')

@app.route('/fitFoodie/report', methods=['GET', 'POST'])
def getDailyReport():
    isPost=False
    if 'loggedin' in session:
       isPost=True
       nutrient = request.form.get('ntrlist')
       period = request.form.get('duration')
       print(nutrient, period)
       today = DT.date.today()
       current_month=today.month
       current_year=today.year
       till_last_date=DT.date.today()
       quantity=[]
       durations=[]
       if(period=='W'):
        till_last_date = today - DT.timedelta(days=7)
        data=[]
        if nutrient=='fat':
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('select sum(fat) as nutr, time from nutrients where u_id=%s and time<=%s and time>=%s group by time order by time', (session['id'],today, till_last_date,))
            data=cursor.fetchall()
        if nutrient=='protein':
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('select sum(protein) as nutr, time from nutrients where u_id=%s and time<=%s and time>=%s group by time order by time', (session['id'],today, till_last_date,))
            data=cursor.fetchall()
        if nutrient=='sodium':
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('select sum(sodium) as nutr, time from nutrients where u_id=%s and time<=%s and time>=%s group by time order by time', (session['id'],today, till_last_date,))
            data=cursor.fetchall()
        if nutrient=='cholesterol':
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('select sum(cholesterol) as nutr, time from nutrients where u_id=%s and time<=%s and time>=%s group by time order by time', (session['id'],today, till_last_date,))
            data=cursor.fetchall()
        print(data)
        for d in data:
            quantity.append(d['nutr'])
            dates=d['time'].strftime("%m/%d/%Y")
            durations.append(dates)
        print(quantity, durations)
       elif(period=='M'):
         till_last_date=DT.datetime(current_year,current_month,1)
         till_last_date=till_last_date.date()
         if nutrient=='fat':
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('select sum(fat) as nutr, time from nutrients where u_id=%s and time<=%s and time>=%s group by time order by time', (session['id'],today, till_last_date,))
            data=cursor.fetchall()
         if nutrient=='protein':
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('select sum(protein) as nutr, time from nutrients where u_id=%s and time<=%s and time>=%s group by time order by time', (session['id'],today, till_last_date,))
            data=cursor.fetchall()
         if nutrient=='sodium':
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('select sum(sodium) as nutr, time from nutrients where u_id=%s and time<=%s and time>=%s group by time order by time', (session['id'],today, till_last_date,))
            data=cursor.fetchall()
         if nutrient=='cholesterol':
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('select sum(cholesterol) as nutr, time from nutrients where u_id=%s and time<=%s and time>=%s group by time order by time', (session['id'],today, till_last_date,))
            data=cursor.fetchall()
         print(data)
         for d in data:
            quantity.append(d['nutr'])
            dates=d['time'].strftime("%m/%d/%Y")
            durations.append(dates)
         print(quantity, durations)
       elif(period=='Y'):
         months=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
         till_last_date=DT.datetime(current_year,1,1)
         till_last_date=till_last_date.date()
         if nutrient=='fat':
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('select sum(fat) as nutr, month(time) as time from nutrients where u_id=%s and  year(time)=%s group by month(time) order by month(time)', (session['id'],current_year,))
            data=cursor.fetchall()
         if nutrient=='protein':
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('select sum(protein) as nutr, month(time) as time from nutrients where u_id=%s and  year(time)=%s group by month(time) order by month(time)', (session['id'],current_year,))
            data=cursor.fetchall()
         if nutrient=='sodium':
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('select sum(sodium) as nutr, month(time) as time from nutrients where u_id=%s and  year(time)=%s group by month(time) order by month(time)', (session['id'],current_year,))
            data=cursor.fetchall()
         if nutrient=='cholesterol':
            cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute('select sum(cholesterol) as nutr, month(time) as time from nutrients where u_id=%s and  year(time)=%s group by month(time) order by month(time)', (session['id'],current_year,))
            data=cursor.fetchall()
         print(data)
         for d in data:
            idx=len(quantity)
            quantity.append(d['nutr'])
            durations.append(months[idx])
         print(quantity, durations)
         
       print(today,till_last_date)
       return render_template('charts.html', quantity=json.dumps(quantity), durations=json.dumps(durations), nutrient=nutrient, period=period,isPost=isPost)
    # else:
    #   if len(quantity)>0:
    #     isPost=True
    #   return render_template('charts.html', isPost=isPost)
    return render_template('charts.html')

if __name__ == "__main__":
    app.run(debug=True)
