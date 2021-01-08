from dotenv import load_dotenv
from flask import Flask, Blueprint, request
from db.database import Client, User, Document, connection, select, delete, insert, update
from werkzeug.utils import secure_filename
import os
import boto3
import botocore
document = Blueprint('Document', __name__, template_folder='templates')
load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWSAccessKeyId'),
    aws_secret_access_key=os.getenv('AWSSecretKey')
)


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
    TESTED - FOUND OK
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
    TESTED - FOUND OK
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
    TESTED - FOUND OK
    Delete the document's Data with a specific id

    Returns:
        Success Message
        OR 
        Empty ID Message
        [type]: [description]
    """
    query = Document.delete().where(Document.columns.id == id)
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        return {'error': 'Unable to find the given document'}
    return {'status': "Delete Succesful"}


@document.route('/<id>', methods=["PUT"])
def updateOne(id):
    """[summary]
    TESTED - FOUND OK
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
    TESTED - FOUND OK
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


@document.route('/file', methods=["POST"])
def addFile():
    """[summary]
    TESTED - FOUND OK
    Upload a Document in S3 and return the URL for the S3

    Returns:
        document data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """

    try:
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join('files', filename))
        f.seek(0)
        output = upload_file_to_s3(f, os.getenv('AWS_bucket_id'))
        try:
            os.remove(os.path.join('files', filename))
        except OSError:
            pass
        return {'url': str(output)}

    except:
        return {'error': 'Unable to Upload the given document'}


@document.route('/file1', methods=["GET,POST"])
def getFile():
    """[summary]
    Download a Document from S3 and return the URL in Local

    Returns:
        document data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    # read data from the API call

    # Read S3 URL,

    # Clear the Download Folder

    # Download the file to folder

    # return the Link to the Downloaded file

    #  CURRENTLY DOWNLOADING USING LINK DIRECTLY

    return {'error': 'Unable to Download the given document'}


def upload_file_to_s3(file, bucket_name, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type  # Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format("https://"+os.getenv('AWS_bucket_id')+".s3.amazonaws.com/", file.filename)
