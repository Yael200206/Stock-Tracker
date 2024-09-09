from flask import Flask, render_template, request, redirect, url_for, flash
from database import Database

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Usamos la clase Database para hacer la consulta
    db = Database()  # Ya no es necesario pasar la configuración, está en database.py
    user = db.fetch_user(username, password)
    
    if user:
        return "Login successful! Welcome " + user['username']
    else:
        flash('Invalid username or password. Please try again.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
