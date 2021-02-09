from flask import Flask, Blueprint, request
from db.database import Reminder, connection, select, delete, insert, update, metadata
import inspect
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
    print(inspect.stack()[1][3])
    op = {}
    for (a, b) in zip((Reminder.c.keys()), list):
         op[a] = str(b).replace('reminder.', '')
    return op


@reminder.route('/test/', methods=["GET", "POST"])
def viewTableAll():
    print(inspect.stack()[1][3])
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
    print(inspect.stack()[1][3])
    query = select([Reminder])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    res = []
    for rs in ResultSet:
        print(rs)
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
    print(inspect.stack()[1][3])
    query = select([Reminder]).where(Reminder.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        print("Unable to find reminder")
        return {'error': 'Unable to find the given Reminder'}
    print(ResultSet)
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
    print(inspect.stack()[1][3])
    query = Reminder.delete().where(Reminder.columns.id == id)
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print("Unable to Delete Reminder")
        return {'error': 'Unable to delete the given Reminder'}
    print("Delete Succesful")
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
    print(inspect.stack()[1][3])
    req_data = request.get_json()
    print(req_data)
    query = select([Reminder]).where(Reminder.columns.id == id)
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print('Unable to Find the given Reminder')
        return {'error': 'Unable to Find the given Reminder'}

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
    if(not ResultProxy):
        print("Unable to Update Reminder")
        return {'error': 'Unable to Update the given Reminder'}
    print("Update Succesful")
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
    print(inspect.stack()[1][3])
    req_data = request.get_json()
    print(req_data)
    json_data = {}

    for req in req_data:
        if (req in Reminder.c.keys()):
            json_data[req] = req_data[req]

    query = (
        insert(Reminder).
        values(json_data)
    )

    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print("Unable to Add Reminder")
        return {'error': 'Unable to Add the given Reminder'}
    print('Adding Reminder Succesful')
    return {'status': "Adding Succesful"}
