from flask import Flask, Blueprint, request
from db.database import Followup, connection, select, delete, insert, update, metadata

followup = Blueprint('followup', __name__, template_folder='templates')


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
    for (a, b) in zip((Followup.c.keys()), list):
         op[a] = str(b).replace('client.', '')
    return op


@followup.route('/test/', methods=["GET", "POST"])
def viewTableAll():
    a = []
    for c in Followup.c:
        a.append(str(c))
    return str(a)


@followup.route('/', methods=["GET", "POST"])
def viewAll():
    """[summary]
    View all the Clients Data

    Returns:
        client data in a String (Do in JSON)
        [type]: [description]
    """
    query = select([Followup])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    res = []
    for rs in ResultSet:
        res.append(list_to_json(rs))
    return dict(enumerate(res))


@followup.route('/<id>', methods=["GET", "POST"])
def viewOne(id):
    """[summary]
    View the Followup's Data with a specific id

    Returns:
        client data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    query = select([Followup]).where(Followup.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to find the given client'}
    return list_to_json(ResultSet)


@followup.route('/<id>', methods=["DELETE"])
def deleteOne(id):
    """[summary]
    Delete the Followup's Data with a specific id

    Returns:
        Success Message
        OR 
        Empty ID Message
        [type]: [description]
    """
    query = Followup.delete().where(Followup.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    if(not ResultSet):
        return {'error': 'Unable to find the given client'}
    return {'status': "Delete Succesful"}


@followup.route('/<id>', methods=["PUT"])
def updateOne(id):
    """[summary]
    Update the Followup's Data with a specific id

    Returns:
        client data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    # read data from the API call
    req_data = request.get_json()

    query = select([Followup]).where(Followup.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to Find the given client'}

    # Update the URL
    json_data = {}

    for req in req_data:
        if (req in Followup.c.keys()):
            json_data[req] = req_data[req]

    query = (
        update(Followup).
        where(Followup.columns.id == id).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        return {'error': 'Unable to Update the given client'}
    return {'status': "Update Succesful"}


@followup.route('/', methods=["PUT"])
def addOne():
    """[summary]
    Add the Followup's Data to an entry

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
        if (req in Followup.c.keys()):
            json_data[req] = req_data[req]

    query = (
        insert(Followup).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        return {'error': 'Unable to Add the given client'}
    return {'status': "Adding Succesful"}
