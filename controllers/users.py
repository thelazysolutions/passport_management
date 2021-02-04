from flask import Flask, Blueprint, request
from db.database import Client, User, connection, select, delete, insert, update, and_

import inspect

user = Blueprint('User', __name__, template_folder='templates')


def list_to_json(list):
    """[summary]
    Appends the Column headers as Keys
    and returns a JSON with the values

    Args:
        list ([type]): [description]

    Returns:
        JSON
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    op = {}
    for (a, b) in zip((User.c.keys()), list):
        op[a] = str(b).replace('user.', '')
    return op


@user.route('/login', methods=['POST'])
def do_login():
    """[summary]
    TESTED - FOUND OK
    User Login API
    query to check if Email & Pwd match

    Returns:
    function call to dashboard
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    req_data = request.get_json()
    print(req_data)
    if('name' in req_data and 'password' in req_data):
        # check for User_type

        query = select([User]).where(and_(User.columns.name ==
                                          req_data['name'], User.columns.password == req_data['password']))
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchone()
        if(not ResultSet):
            print('Unable to find the user for Login')
            return {'error': 'Unable to find the user for Login'}

        print(list_to_json(ResultSet))
        return {'success': ' User logs in', 'user_id': list_to_json(ResultSet)}

    print('Cannot login')
    return {'error': 'Cannot Login'}


@user.route('/', methods=["GET", "POST"])
def viewAll():
    """[summary]
    TESTED - FOUND OK
    View all the user Data

    Returns:
        user data in a String (Do in JSON)
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    query = select([User])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    res = []
    for rs in ResultSet:
        print(rs)
        res.append(list_to_json(rs))
    return dict(enumerate(res))


@user.route('/<id>', methods=["GET", "POST"])
def viewOne(id):
    """[summary]
    TESTED - FOUND OK
    View the user's Data with a specific id

    Returns:
        user data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    query = select([User]).where(User.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to find the given user'}
    print(ResultSet)
    return list_to_json(ResultSet)


@user.route('/<id>', methods=["DELETE"])
def deleteOne(id):
    """[summary]
    TESTED - FOUND OK
    Delete the user's Data with a specific id

    Returns:
        Success Message
        OR 
        Empty ID Message
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    query = User.delete().where(User.columns.id == id)
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print('Unable to find the given user')
        return {'error': 'Unable to find the given user'}
    print("Delete Succesful for ID: " + str(id))
    return {'status': "Delete Succesful for ID: " + str(id)}


@user.route('/<id>', methods=["PUT"])
def updateOne(id):
    """[summary]
    TESTED - FOUND OK
    Update the user's Data with a specific id

    Returns:
        user data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    # read data from the API call
    req_data = request.get_json()
    print(req_data)
    query = select([User]).where(User.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to find the given user'}

    json_data = {}

    for req in req_data:
        if (req in User.c.keys()):
            json_data[req] = req_data[req]

    if(json_data != {}):

        query = (
            update(User).
            where(User.columns.id == id).
            values(json_data)
        )
        ResultProxy = connection.execute(query)
        if(not ResultProxy):
            print('Unable to Update the given user')
            return {'error': 'Unable to Update the given user'}
        print("Update Succesful for object "+id)
        return {'status': "Update Succesful for object "+id}
    print("No new entries to be updated")
    return {'status': "No new entries to be updated"}


@user.route('/', methods=["PUT"])
def addOne():
    """[summary]
    TESTED - FOUND OK
    Add the user's Data to an entry

    Returns:
        user data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    # read data from the API call
    print(inspect.stack()[1][3])
    req_data = request.get_json()
    print(req_data)
    if(req_data):
        if('name' in req_data and 'email' in req_data and 'password' in req_data and 'user_type' in req_data):
            query = (
                insert(User).
                values(req_data)
            )
            ResultProxy = connection.execute(query)
            if(not ResultProxy):
                print('Unable to Add the given user')
                return {'error': 'Unable to Add the given user'}
            print("Adding Succesful")
            return {'status': "Adding Succesful"}

    return {'error': 'Cannot add new value'}
