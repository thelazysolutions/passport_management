from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, get_flashed_messages, jsonify, Blueprint
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, MetaData, Table, Column, select, insert, and_, update
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(12)


engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
connection = engine.connect()
metadata = MetaData()
Client = Table('client', metadata,
                  autoload=True, autoload_with=engine,extend_existing=True)
User = Table('user', metadata,
                  autoload=True, autoload_with=engine,extend_existing=True)


@app.route('/')
def home(result=None):
    print(not session.get('logged_in') and not result)
    if not session.get('logged_in') and not result:
        return render_template('login.html')
    else:
        # Based on the user_id passed, print Details, URLS and all.
        # return render_template('dashboard.html', username=result.name, user_id=result.user_type)
        return render_template('webpage/index1.html', username=result.name, user_id=result.user_type)
    
@app.route('/test')
def test(done = None):
    if(done):
        flash('New Entry Done!')
    return render_template('webpage/index1.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    # query to check if Email & Pwd match

    query = select([User]).where(and_(User.columns.email == request.form['email'],User.columns.password==request.form['password'] ))
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    result = ResultSet
    # result = User.query.filter_by(
    #     password=request.form['password'], email=request.form['email']).first()
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

@app.route('/foo', methods=['POST']) 
def foo():
    print(request.form)
    data = request.form.to_dict()
    print(data)
    return test('done')

if __name__ == "__main__":
    app.run(debug=True)
