from flask import Flask, Blueprint, request
from db.database import Client, connection, select, delete, insert, update, metadata

client = Blueprint('client', __name__, template_folder='templates')


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
    for (a, b) in zip((Client.c.keys()), list):
        op[a] = str(b).replace('client.', '')
    return op


@client.route('/test/', methods=["GET", "POST"])
def viewTableAll():
    obj = {}
    for key in Client.c.keys():
        obj[key] = '1'
    return obj


@client.route('/', methods=["GET", "POST"])
def viewAll():
    """[summary]
    TESTED - FOUND OK
    View all the Clients Data

    Returns:
        client data in a String (Do in JSON)
        [type]: [description]
    """
    query = select([Client])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    res = []
    for rs in ResultSet:
        res.append(list_to_json(rs))
    return dict(enumerate(res))


@client.route('/<id>', methods=["GET", "POST"])
def viewOne(id):
    """[summary]
    TESTED - FOUND OK
    View the Client's Data with a specific id

    Returns:
        client data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    query = select([Client]).where(Client.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to find the given client'}
    return list_to_json(ResultSet)


@client.route('/<id>', methods=["DELETE"])
def deleteOne(id):
    """[summary]
    TESTED - FOUND OK
    Delete the Client's Data with a specific id

    Returns:
        Success Message
        OR 
        Empty ID Message
        [type]: [description]
    """
    query = Client.delete().where(Client.columns.id == id)
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        return {'error': 'Unable to find the given client'}
    return {'status': "Delete Succesful"}


@client.route('/<id>', methods=["PUT"])
def updateOne(id):
    """[summary]
    TESTED - FOUND OK
    Update the Client's Data with a specific id

    Returns:
        client data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    # read data from the API call
    req_data = request.get_json()

    query = select([Client]).where(Client.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to Find the given client'}

    # Update the URL
    json_data = {}

    for req in req_data:
        if (req in Client.c.keys()):
            json_data[req] = req_data[req]

    query = (
        update(Client).
        where(Client.columns.id == id).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        return {'error': 'Unable to Update the given client'}
    return {'status': "Update Succesful"}


@client.route('/', methods=["PUT"])
def addOne():
    """[summary]
    TESTED - FOUND OK
    Add the Client's Data to an entry

    Returns:
        client data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    # read data from the API call
    req_data = request.get_json()
    json_data = {}

    for req in req_data:
        if (req in Client.c.keys()):
            json_data[req] = req_data[req]

    query = (
        insert(Client).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        return {'error': 'Unable to Add the given client'}
    return {'status': "Adding Succesful"}
