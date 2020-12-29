from flask import Flask, Blueprint, request
from db.database import Client, User, connection, select, delete, insert, update

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
    op = []
    for (a, b) in zip((User.c.keys()),list):
        # print(a,b) 
        op.append({a:str(b).replace('user.','')})
    return op


@user.route('/', methods=["GET", "POST"])
def viewAll():
    """[summary]
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
        return {'error':'Unable to find the given user'}
    return list_to_json(ResultSet)


@user.route('/<id>', methods=["DELETE"])
def deleteOne(id):
    """[summary]
    Delete the user's Data with a specific id

    Returns:
        Success Message
        OR 
        Empty ID Message
        [type]: [description]
    """
    query = User.delete().where(User.columns.id == id)
    ResultProxy = connection.execute(query)
    print(ResultProxy)
    ResultSet = ResultProxy.fetchall()
    if(not ResultSet):
        return {'error':'Unable to find the given user'}
    return {'status':"Delete Succesful"}


@user.route('/<id>', methods=["PUT"])
def updateOne(id):
    """[summary]
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
        return {'error':'Unable to find the given user'}

    if('name' in req_data or 'email' in req_data or 'pwd' in req_data or 'user_type' in req_data):

        query = (
            update(User).
            where(User.columns.id == id).
            values(req_data)
        )
        ResultProxy = connection.execute(query)
        if(not ResultProxy):
            return {'error':'Unable to Update the given user'} 
        return {'status':"Update Succesful"}

    return {'status':"No new entries to be updated"}


@user.route('/', methods=["PUT"])
def addOne():
    """[summary]
    Add the user's Data to an entry

    Returns:
        user data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    # read data from the API call
    req_data = request.get_json()

    if('name' in req_data and 'email' in req_data and 'pwd' in req_data and 'user_type' in req_data):
        # check for User_type

        query = (
            insert(User).
            values(name=req_data['name'], email=req_data['email'],
                   password=req_data['pwd'], user_type=req_data['user_type'])
        )
        ResultProxy = connection.execute(query)
        if(not ResultProxy):
            return {'error':'Unable to Add the given user'} 
        return {'status':"Adding Succesful"}

    return {'error':'Cannot add new value'}  
