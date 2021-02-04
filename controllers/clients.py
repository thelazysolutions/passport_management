from flask import Flask, Blueprint, request
from db.database import Client, connection, select, delete, insert, update, metadata
import inspect
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
    print(inspect.stack()[1][3])
    op = {}
    for (a, b) in zip((Client.c.keys()), list):
        op[a] = str(b).replace('client.', '')
    return op


@client.route('/test/', methods=["GET", "POST"])
def viewTableAll():
    print(inspect.stack()[1][3])
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
    print(inspect.stack()[1][3])
    query = select([Client])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    res = []
    for rs in ResultSet:
        print(rs)
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
    print(inspect.stack()[1][3])
    query = select([Client]).where(Client.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to find the given client'}
    print(ResultSet)
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
    print(inspect.stack()[1][3])
    query = Client.delete().where(Client.columns.id == id)
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print('Unable to find the given client')
        return {'error': 'Unable to find the given client'}
    print("Delete Succesful for ID: " + str(id))
    return {'status': "Delete Succesful for ID: " + str(id)}


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
    print(inspect.stack()[1][3])
    req_data = request.get_json()
    print(req_data)
    query = select([Client]).where(Client.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        print('Unable to find the given client')
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
        print("unable to update client")
        return {'error': 'Unable to Update the given client'}
    print("Update Succesful")
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
    print(inspect.stack()[1][3])
    req_data = request.get_json()
    print(req_data)
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
        print("Unable to Add Client")
        return {'error': 'Unable to Add the given client'}
    print("Add Succesful")
    return {'status': "Adding Succesful"}
