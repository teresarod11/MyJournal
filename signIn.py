from flask import Flask, request, render_template, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,template_folder='templates')
app.secret_key = 'your-secret-key'

# MySQL configurations
db_config = {
    'host': 'localhost',
    'user': '',
    'password': '',
    'database': ''
}

# Create a MySQL connection
conn = mysql.connector.connect(**db_config)

@app.route('/signUp', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='sha256')

        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
            (username, email, hashed_password)
        )
        conn.commit()
        cursor.close()

        flash('Registration successful. Please log in.')
        return redirect(url_for('index'))

    return render_template('signUp.html')

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))

        flash('Login failed. Check your credentials.')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
