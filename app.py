from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, get_flashed_messages
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(12)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Defination of Schema
# Need to Move this to separate python file


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    user_type = db.Column(db.Integer, unique=False, nullable=False)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    number = db.Column(db.String, unique=True, nullable=False)
    number_alt = db.Column(db.String, unique=True, nullable=True)
    email = db.Column(db.String, unique=True, nullable=False)
    email_alt = db.Column(db.String, unique=True, nullable=False)
    number_alt = db.Column(db.String, unique=True, nullable=True)
    location = db.Column(db.String, unique=True, nullable=False)
    source = db.Column(db.String, unique=True, nullable=False)
    referred_by = db.Column(db.String, unique=True, nullable=True)
    process_type = db.Column(db.String, unique=True, nullable=False)
    first_registration_of = db.Column(db.String, unique=True, nullable=False)
    lead_type = db.Column(db.String, unique=True, nullable=True)
    assigned_to = db.Column(db.String, unique=True, nullable=False)
    search_location = db.Column(db.String, unique=True, nullable=False)
    search_taluka = db.Column(db.String, unique=True, nullable=True)
    wa_group_name = db.Column(db.String, unique=True, nullable=False)
    search_required = db.Column(db.Boolean, unique=True, nullable=False)
    wa_group = db.Column(db.Boolean, unique=True, nullable=True)
    first_contact_date = db.Column(db.DateTime, unique=True, nullable=False)
    


@app.route('/')
def home(result=None):
    print(not session.get('logged_in') and not result)
    if not session.get('logged_in') and not result:
        return render_template('login.html')
    else:
        # Based on the user_id passed, print Details, URLS and all.
        # return render_template('dashboard.html', username=result.name, user_id=result.user_type)
        return render_template('dash/index.html', username=result.name, user_id=result.user_type)
    
@app.route('/test')
def test():
    return render_template('dash/index.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    # query to check if Email & Pwd match
    result = User.query.filter_by(
        password=request.form['password'], email=request.form['email']).first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
        # return str(get_flashed_messages())
    return home(result)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


if __name__ == "__main__":
    app.run(debug=True)
