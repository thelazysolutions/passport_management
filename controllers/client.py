from flask import Flask, Blueprint, request
from db.database import Client, User, connection, select, delete

client = Blueprint('client', __name__, template_folder='templates')


@client.route('/', methods=["GET", "POST"])
def viewAll():
    """[summary]
    View all the Clients Data

    Returns:
        client data in a String (Do in JSON)
        [type]: [description]
    """
    query = select([User])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    return str(ResultSet)


@client.route('/<id>', methods=["GET", "POST"])
def viewOne(id):
    """[summary]
    View the Client's Data with a specific id

    Returns:
        client data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    query = select([User]).where(User.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return "empty set"
    return str(ResultSet)



@client.route('/<id>', methods=["DELETE"])
def deleteOne(id):
    """[summary]
    Delete the Client's Data with a specific id

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
        return "Couldn't find entry to Delete"
    return "Delete Succesful"


@client.route('/<id>', methods=["PUT"])
def updateOne(id):
    """[summary]
    Update the Client's Data with a specific id

    Returns:
        client data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    # read data from the API call
    req_data = request.get_json()
    print(req_data)

    query = select([User]).where(User.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return "empty set"
    
    # Read from the JSON
    # Save query data into another JSON
    # update it with the JSON of Request
    # Update into the DB
    # return str(ResultSet)
    return str(req_data)

@client.route('/', methods=["PUT"])
def addOne():
    """[summary]
    Add the Client's Data to an entry

    Returns:
        client data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    # read data from the API call
    req_data = request.get_json()
    print(req_data)
    # if all info filled, Create new user
    # query = select([User]).where(User.columns.id == id)
    # ResultProxy = connection.execute(query)
    # ResultSet = ResultProxy.fetchone()
    # if(not ResultSet):
    #     return "empty set"
    # return str(ResultSet)
    return str(req_data)