from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, get_flashed_messages, jsonify, Blueprint
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
from controllers.users import user
from controllers.clients import client
from controllers.document import document
from controllers.reminder import reminder
from controllers.followup import followup
from sqlalchemy import create_engine, MetaData, Table, Column, select, insert, and_, update

from db.database import Client,User,connection
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(12)
cors = CORS(app)
app.register_blueprint(user, url_prefix='/user/')
app.register_blueprint(client, url_prefix='/client/')
app.register_blueprint(document, url_prefix='/document/')
app.register_blueprint(reminder, url_prefix='/reminder/')
app.register_blueprint(followup, url_prefix='/followup/')

@app.route('/')
def home(result=None):
    """[summary]
    Homepage - Redirect to Login

    Args:
        result to redirect to the dashboard
        result ([type], optional): [description]. Defaults to None.

    Returns:
        render_template
        [type]: [description]
    """
    if not session.get('logged_in') and not result:
        return render_template('login.html')
    else:
        # Based on the user_id passed, print Details, URLS and all.
        # return render_template('dashboard.html', username=result.name, user_id=result.user_type)
        return render_template('webpage/index1.html', username=result.name, user_id=result.user_type)
    
@app.route('/test')
def test(done = None):
    """[summary]
    testing function to check render_template
    Args:
        done ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    if(done):
        flash('New Entry Done!')
    return render_template('webpage/index1.html')


@app.route('/login', methods=['POST'])
def do_login_login():
    """[summary]
    query to check if Email & Pwd match
    Testing for demo frontend
    DO NOT USE
    Returns:
    function call to dashboard
        [type]: [description]
    """

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
    """[summary]
    logout functionality
    Returns:
        home() ==> Login page
        [type]: [description]
    """
    session['logged_in'] = False
    return home()

@app.route('/foo', methods=['POST']) 
def foo():
    """[summary]
    testing for reading data from a form

    Returns:
    function call to test page
        [type]: [description]
    """
    print(request.form)
    data = request.form.to_dict()
    print(data)
    return test('done')

if __name__ == "__main__":
    app.run(debug=True)
