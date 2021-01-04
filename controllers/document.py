from flask import Flask, Blueprint, request
from db.database import Client, User, Document, connection, select, delete, insert, update

document = Blueprint('Document', __name__, template_folder='templates')


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
    for (a, b) in zip((Document.c.keys()), list):
        op[a] = str(b).replace('document.', '')
    return op


@document.route('/test', methods=["GET", "POST"])
def test():
    obj = {}
    for key in Document.c.keys():
        obj[key] = '1'
    return obj

@document.route('/', methods=["GET", "POST"])
def viewAll():
    """[summary]
    View all the document Data

    Returns:
        document data in a String (Do in JSON)
        [type]: [description]
    """
    query = select([Document])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    res = []
    for rs in ResultSet:
        res.append(list_to_json(rs))
    return dict(enumerate(res))


@document.route('/<id>', methods=["GET", "POST"])
def viewOne(id):
    """[summary]
    View the document's Data with a specific id

    Returns:
        document data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    query = select([Document]).where(Document.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to find the given document'}
    return list_to_json(ResultSet)


@document.route('/<id>', methods=["DELETE"])
def deleteOne(id):
    """[summary]
    Delete the document's Data with a specific id

    Returns:
        Success Message
        OR 
        Empty ID Message
        [type]: [description]
    """
    query = Document.delete().where(Document.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    if(not ResultSet):
        return {'error': 'Unable to find the given document'}
    return {'status': "Delete Succesful"}


@document.route('/<id>', methods=["PUT"])
def updateOne(id):
    """[summary]
    Update the document's Data with a specific id

    Returns:
        document data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    # read data from the API call
    req_data = request.get_json()

    query = select([Document]).where(Document.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to find the given document'}

    json_data = {}

    for req in req_data:
        if (req in Document.c.keys()):
            json_data[req] = req_data[req]

    if(json_data != {}):

        query = (
            update(Document).
            where(Document.columns.id == id).
            values(json_data)
        )
        ResultProxy = connection.execute(query)
        if(not ResultProxy):
            return {'error': 'Unable to Update the given document'}
        return {'status': "Update Succesful"}

    return {'status': "No new entries to be updated"}


@document.route('/', methods=["PUT"])
def addOne():
    """[summary]
    Add the document's Data to an entry

    Returns:
        document data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    # read data from the API call
    req_data = request.get_json()
    # check for Document_type

    json_data = {}

    for req in req_data:
        if (req in Document.c.keys()):
            json_data[req] = req_data[req]

    if(json_data != {}):

        query = (
            insert(Document).
            values(json_data)
        )
        ResultProxy = connection.execute(query)
        if(not ResultProxy):
            return {'error': 'Unable to Add the given document'}
        return {'status': "Adding Succesful"}
    return {'error': 'Unable to Add the given document'}

