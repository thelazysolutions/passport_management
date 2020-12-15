from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello User!  <a href=\"/logout\">Logout</a>"

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == "__main__":
    
    app.run(debug=True)