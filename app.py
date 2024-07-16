from flask import Flask, render_template, request, redirect, url_for, session, flash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
import os
import mysql.connector



app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

# Configurations for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')



# Database configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'project'
}

def create_database_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Example: Inserting data into MySQL
        connection = create_database_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already taken. Please choose a different one.', 'error')
            return redirect(url_for('create_account'))

        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('login'))  # Redirect to login page after account creation
    else:
        return render_template('signup.html')  # Render the create account form
    
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = create_database_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/course1')
def course1():
    session.pop('username', None)
    return render_template('course1.html')

@app.route('/course2')
def course2():
    session.pop('username', None)
    return render_template('course2.html')

@app.route('/course3')
def course3():
    session.pop('username', None)
    return render_template('course3.html')

@app.route('/mock_test')
def mock_test():
    if 'username' in session:
        return render_template('mock_test.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)