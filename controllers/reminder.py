from flask import Flask, Blueprint, request
from db.database import Reminder, connection, select, delete, insert, update, metadata

reminder = Blueprint('reminder', __name__, template_folder='templates')


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
    for (a, b) in zip((Reminder.c.keys()), list):
         op[a] = str(b).replace('client.', '')
    return op


@reminder.route('/test/', methods=["GET", "POST"])
def viewTableAll():
    a = []
    for c in Reminder.c:
        a.append(str(c))
    return str(a)


@reminder.route('/', methods=["GET", "POST"])
def viewAll():
    """[summary]
    View all the Clients Data

    Returns:
        client data in a String (Do in JSON)
        [type]: [description]
    """
    query = select([Reminder])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    res = []
    for rs in ResultSet:
        res.append(list_to_json(rs))
    return dict(enumerate(res))


@reminder.route('/<id>', methods=["GET", "POST"])
def viewOne(id):
    """[summary]
    View the Reminder's Data with a specific id

    Returns:
        client data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    query = select([Reminder]).where(Reminder.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to find the given client'}
    return list_to_json(ResultSet)


@reminder.route('/<id>', methods=["DELETE"])
def deleteOne(id):
    """[summary]
    Delete the Reminder's Data with a specific id

    Returns:
        Success Message
        OR 
        Empty ID Message
        [type]: [description]
    """
    query = Reminder.delete().where(Reminder.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    if(not ResultSet):
        return {'error': 'Unable to find the given client'}
    return {'status': "Delete Succesful"}


@reminder.route('/<id>', methods=["PUT"])
def updateOne(id):
    """[summary]
    Update the Reminder's Data with a specific id

    Returns:
        client data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    # read data from the API call
    req_data = request.get_json()

    query = select([Reminder]).where(Reminder.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to Find the given client'}

    # Update the URL
    json_data = {}

    for req in req_data:
        if (req in Reminder.c.keys()):
            json_data[req] = req_data[req]

    query = (
        update(Reminder).
        where(Reminder.columns.id == id).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    if(not ResultSet):
        return {'error': 'Unable to Update the given client'}
    return {'status': "Update Succesful"}


@reminder.route('/', methods=["PUT"])
def addOne():
    """[summary]
    Add the Reminder's Data to an entry

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
        if (req in Reminder .c.keys()):
            json_data[req] = req_data[req]

    query = (
        insert(Reminder).
        values(json_data)
    )

    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        return {'error': 'Unable to Add the given client'}
    return {'status': "Adding Succesful"}
