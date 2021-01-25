from flask import Flask, Blueprint, request
from db.database import Client, User, connection, select, delete, insert, update, and_

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
    req_data = request.get_json()

    if('name' in req_data and 'password' in req_data):
        # check for User_type

        query = select([User]).where(and_(User.columns.name ==
                                          req_data['name'], User.columns.password == req_data['password']))
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchone()
        if(not ResultSet):
            return {'error': 'Unable to find the user for Login'}

        return {'success': ' User logs in', 'user_id': list_to_json(ResultSet)}

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
    query = select([User])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    res = []
    for rs in ResultSet:
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
    query = select([User]).where(User.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to find the given user'}
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
    query = User.delete().where(User.columns.id == id)
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        return {'error': 'Unable to find the given user'}
    return {'status': "Delete Succesful"}


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
    # read data from the API call
    req_data = request.get_json()

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
            return {'error': 'Unable to Update the given user'}
        return {'status': "Update Succesful for object "+id}

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
    req_data = request.get_json()

    if(req_data):
        if('name' in req_data and 'email' in req_data and 'password' in req_data and 'user_type' in req_data):
            # check for User_type

            query = (
                insert(User).
                values(req_data)
            )
            ResultProxy = connection.execute(query)
            if(not ResultProxy):
                return {'error': 'Unable to Add the given user'}
            return {'status': "Adding Succesful"}

    return {'error': 'Cannot add new value'}
